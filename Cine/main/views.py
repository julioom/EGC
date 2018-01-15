# encoding: UTF-8

import shelve
from main.models import User, Film,Genre, Rating
from main.forms import UserForm, GenreForm, FilmForm, SynopsisForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches
from main.populate import populateDatabase
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
import os
import urllib2
import numpy as np #crear ficheros CSV

dirindex = "Index_temas"
ruta="Cine\\csv\\"
Prefs={}   # matriz de usuarios y puntuaciones a cada a items
ItemsPrefs={}   # matriz de items y puntuaciones de cada usuario. Inversa de Prefs
SimItems=[]  # matriz de similitudes entre los items

def loadDict():
    shelf = shelve.open("Cine\\dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = ra.user.idUser
        itemid = ra.film.idMovie
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()
    
def get_schema_peliculas():
    return Schema(id=TEXT(stored=True), titulo=TEXT(stored=True), director=TEXT(stored=True),
                  reparto=TEXT(stored=True),sinopsis=TEXT(stored=True),url = TEXT(stored=True),fecha_estreno=TEXT(stored=True),
                  medios=TEXT(stored=False),usuarios=TEXT(stored=False),sensacine=TEXT(stored=False),
                  generos=KEYWORD(stored=True))
    

    
def crear_indices_peliculas():
    datos = crearPelis()

    if datos:  # Comprueba si contiene algo
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    else:
        print("No se ha extraido ningun dato")
        return

    ix_peliculas = create_in(dirindex, schema=get_schema_peliculas())
    writer = ix_peliculas.writer()

    peliculas_i = 0
    for dato in datos:
        ide,tit,dir,rep,sin,fecha,enlace,med,usu,sen,gen=dato
        list_generos=[]
        gene = gen.split(',')
        for g in gene:
            genero=g.decode('utf-8')
            list_generos.append(genero)
        print sin
        writer.add_document(id=ide.decode('utf-8'), titulo=tit.decode('utf-8'), director=dir.decode('utf-8'),reparto=rep.decode('utf-8'),
                            sinopsis=sin.decode('utf-8'),fecha_estreno=fecha.decode('utf-8'),
                            url = enlace.decode('utf-8'),medios=med.decode('utf-8'),
                            usuarios=usu.decode('utf-8'),sensacine=sen.decode('utf-8'),generos=list_generos)#, puntuaciones=pun)
        peliculas_i += 1

    writer.commit()

    print ("Indexar", "Se han indexado {} Peliculas".format(peliculas_i))
    
# Create your views here.

def index(request): 
    #crear_indices_peliculas()
    return render_to_response('index.html')

def populateDB(request):
    populateDatabase() 
    return render_to_response('populate.html')

def loadRS(request):
    loadDict()
    return render_to_response('loadRS.html')

#Crear CSV con Beautifulsoup
        
def crearPelis():
    datos = []
    links = []
    completo = []
    
    for indice in range(1):
        pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/mejores/nota-espectadores/?page="+str(indice+1))
        soup = BeautifulSoup(pagina, 'html.parser')
        
        link_pel="http://www.sensacine.com"
        all_links = soup.find_all(class_='no_underline')
        for l in all_links:
            link = link_pel + l.get('href')
            links.append(link)
            
    for e in links:
        pagina = urllib2.urlopen(e)
        soup = BeautifulSoup(pagina, 'html.parser')
        
        #Recogida de ID    
        href = soup.find(class_='home item current').get('href').split('/')
        id_compl = href[2].split('-')
        ide = id_compl[1].encode('utf-8')
                  
        #Recogida de titulo
        titulo = soup.find('div',class_='titlebar-title').text.encode('utf-8')
        #u' '.join(titulo).encode('utf-8').strip()
        
        #trailer
        href = soup.find(class_="trailer item").get("href")
        enlace = "http://www.sensacine.com"+href
        pagina2 = urllib2.urlopen(enlace)
        soup2 = BeautifulSoup(pagina2, 'html.parser')
        todo= soup2.find(id="player-export").get("data-model")
        partes = todo.split('"')
        url = partes[7].replace("\\","")
        print url
        url.encode('utf-8')
        print url
         
        div= soup.find_all('div',class_='meta-body-item')
            
        #Comprobar si tiene fecha de re-estreno porque asi los divs son distintos
        i=0
        if soup.find(class_='meta-body-item').span.text == "Fecha de re-estreno":
            i=1
        #Recogida de fecha
        fecha = div[0+i].find(class_='date').text.encode('utf-8')
                
        #Recogida de Genero
        list_gen = []
        lista=[]
        gene= ""
        generos = div[3+i].find_all(class_='blue-link')
        for g in generos:
            lista.append(g.text)
            list_gen.append(g.text)
        gene+=','.join(lista).encode('utf-8')
      
        #u' '.join(gene).encode('utf-8').strip()
        
        #Recogida de Directores
        list_direc =[]
        lista2 =[]
        dire=""
        directores = div[i+1].find_all(itemprop='director')
        for d in directores:
            texto = d.text.replace(',',' ').strip().split('\n')
            for t in texto:
                lista2.append(t)
            
        dire+=','.join(lista2).encode('utf-8')
        print dire
          
        #Recogida de Reparto
        rep=""
        list_act=[]
        reparto = div[2+i].find_all('span')
        actores= reparto[1:len(reparto)-1]
        for a in actores:
            #rep+=a.text+","
            list_act.append(a.text)
        rep+=",".join(list_act).encode('utf-8') 
         
        #Recogida de Synopsis
        synopsis = soup.find(class_='synopsis-txt').text.strip().encode('utf-8')
        
            #Recogida de votos
        votos = soup.find_all(class_='rating-item')
        votos_usuarios = ""
        votos_medios = ""
        votos_sensacine = ""
        for voto in votos:
            puntuacion =  voto.find(class_='rating-title').text.strip()
            if puntuacion == "Usuarios":
                votos_usuarios = voto.find(class_='stareval-note').text.strip().encode('utf-8')          
                               
            elif puntuacion == "Medios":
                votos_medios = voto.find(class_='stareval-note').text.strip().encode('utf-8')
                    
            elif puntuacion == "Sensacine":
                votos_sensacine = voto.find(class_='stareval-note').text.strip().encode('utf-8')
                    
        #datos.append([ide,titulo,dire,rep,synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine,gene])        
        datos.append([ide,titulo,dire,rep,"",fecha,url,votos_usuarios, votos_medios, votos_sensacine,gene])
        completo.append([ide,titulo,dire,rep,synopsis,fecha,url,votos_usuarios, votos_medios, votos_sensacine,gene])
         
    print "---------------------------------------------------"
    todo = np.asarray(datos)
    np.savetxt(ruta+'films.csv', #ruta+"films.csv",   # Archivo de salida
           todo,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter="|")
    
    return completo
    

def crearUsuarios():
    
    fileobj=open(ruta+'films.csv', "r")
    line=fileobj.readline()
    ids_films=[]
    usuarios=[]
    puntuaciones=[]
    while line:
        
        ide = line.split('|')[0].strip().decode('utf-8', 'replace')
        if ide.isdigit():
            ids_films.append(ide)
        line=fileobj.readline()
    fileobj.close()
    
    for id_film in ids_films:
        pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/pelicula-"+id_film+"/criticas-espectadores/")
        soup = BeautifulSoup(pagina, 'html.parser')
        
        todos_usuarios = soup.find_all(class_='row item hred')
        for u in todos_usuarios:
            ide = u.find(class_='item-profil')
            if ide:
                idee=ide.get('data-targetuserid').encode('utf-8')
            nombre = u.find(itemprop='author')
            if nombre:
                nombree = nombre.text.encode('utf-8')
            if [idee,nombree] not in usuarios:
                usuarios.append([idee,nombree])
                
            valor = u.find(itemprop="ratingValue").text.strip()
            fecha = u.find(class_='review-about light').text.strip().split()[2]
            
            puntuaciones.append([idee,id_film,fecha,valor])
        
    todo = np.asarray(usuarios)
    np.savetxt(ruta+'users.csv', #ruta+"films.csv",   # Archivo de salida
           todo,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter=",")
    
    todo2 = np.asarray(puntuaciones)
    np.savetxt(ruta+'ratings.csv', #ruta+"films.csv",   # Archivo de salida
           todo2,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter="|")

    
def crearGeneros():
    datos = []
    pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/mejores/nota-espectadores/")
    soup = BeautifulSoup(pagina, 'html.parser')
    
    columna = soup.find('div',class_='left_col_menu_item')

    generos = columna.find_all('li')[1:]
    for g in generos:
        genero = g.text.split('(')[0].strip().encode('utf-8')
        print genero
        datos.append(genero)
        
    todo = np.asarray(datos)
    np.savetxt(ruta+"genres.csv",   # Archivo de salida
           todo,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter=",")

def crearCSV(request):
    crearPelis()
    #crear_indices_peliculas()
    #crearUsuarios()
    #crearGeneros()
    
    return render_to_response('index.html')
    
def searchByGenre(request): #con whoosh
    if request.method=='GET':
        form = GenreForm(request.GET, request.FILES)
        peliculas=[]
        if form.is_valid():
            genre = form.cleaned_data['genre']
            ix = open_dir(dirindex)
            with ix.searcher() as searcher:
                query = QueryParser("generos", ix.schema).parse(unicode(genre))
                results = searcher.search(query)
                print results
                for r in results:
                    peliculas.append(r)
                return render_to_response('films_by_genre.html', {'genre':genre,'peliculas':peliculas})
    else:
        form=GenreForm()
    return render_to_response('search_genre.html', {'form':form }, context_instance=RequestContext(request))

def searchBySynopsis(request): #con whoosh
    if request.method=='GET':
        form = SynopsisForm(request.GET, request.FILES)
        movies=[]
        if form.is_valid():
            word = form.cleaned_data['word'] 
            ix = open_dir(dirindex)
            with ix.searcher() as searcher:
                query = QueryParser("sinopsis", ix.schema).parse(unicode(word))
                results = searcher.search(query)
                print results
                for r in results:
                    movies.append(r)
                print movies        
                return render_to_response('films_by_synopsis.html', {'word':word,'movies':movies})
    else:
        form=SynopsisForm()
    return render_to_response('search_synopsis.html', {'form':form }, context_instance=RequestContext(request))

def peliculas_por_genero(request): #con django
    peliculas = []
    if request.method=='GET':
        form = GenreForm(request.GET, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['genre']
            genre = get_object_or_404(Genre, pk=nombre)
            for f in Film.objects.filter(genres=genre):
                peliculas.append(f)
            #url="//s3.vid.web.acsta.net/ES/nmedia/35/18/68/09/14/19425076_sd_013.mp4"
            return render_to_response('films_by_genre.html', {'genre': genre,'peliculas': peliculas}, context_instance=RequestContext(request))
    form = GenreForm()
    return render_to_response('search_genre.html', {'form': form}, context_instance=RequestContext(request))

def searchByUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['name']
            usuario = get_object_or_404(User, name=nombre)
            print usuario
            return render_to_response('ratedFilms.html', {'usuario':usuario})
    else:
        form=UserForm()
    return render_to_response('search_user.html', {'form':form }, context_instance=RequestContext(request))

#Recomienda dos peliculas a un usuario que no haya puntuado
def recommendedFilms(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['name']
            user = get_object_or_404(User, name=nombre)
            print user.idUser
            shelf = shelve.open("Cine\\dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()     
            rankings = getRecommendedItems(Prefs, SimItems, user.idUser)
            recommended = rankings[:2]
            items = []
            print rankings
            print recommended
            print "------"
            for re in recommended:
                print re
                item = Film.objects.get(idMovie=re[1])
                items.append(item)
            print items
            print user 
            return render_to_response('recommendationItems.html', {'user': user, 'items': items}, context_instance=RequestContext(request))
    form = UserForm()
    return render_to_response('search_user.html', {'form': form}, context_instance=RequestContext(request))

#Recomienda 3 peliculas similares a la dada
def similarFilms(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = int(form.cleaned_data['id'])
            film = get_object_or_404(Film, idMovie=idFilm)
            shelf = shelve.open("Cine\\dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, idFilm,n=3)
            items=[]
            for re in recommended:
                print re
                print re[1]
                item = Film.objects.get(idMovie=re[1])
                items.append(item)
            return render_to_response('similarFilms.html', {'film': film,'films': items}, context_instance=RequestContext(request))
    form = FilmForm()
    return render_to_response('search_film.html', {'form': form}, context_instance=RequestContext(request))



