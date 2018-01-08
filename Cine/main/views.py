# encoding: UTF-8

import shelve
from main.models import User, Film,Genre, Rating
from main.forms import UserForm, GenreForm, FilmForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches
from main.populate import populateDatabase
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
import tkMessageBox
import os
import urllib2
import numpy as np #crear ficheros CSV
import csv

dirindex = "Index_temas"
ruta="Cine//csv//"
Prefs={}   # matriz de usuarios y puntuaciones a cada a items
ItemsPrefs={}   # matriz de items y puntuaciones de cada usuario. Inversa de Prefs
SimItems=[]  # matriz de similitudes entre los items

def loadDict():
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.film.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()
    
def get_schema_peliculas():
    return Schema(id=TEXT(stored=True), titulo=TEXT(stored=True), fecha_publicacion=TEXT(stored=True),
                  generos=KEYWORD(stored=True))#, puntuaciones=KEYWORD(stored=True))
    

    
def crear_indices_peliculas():
    datos = ""#extraer_datos("http://mk2films.com/en/catalogues/international-en/")

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
        i,tit,fec,gen,pun=dato
        writer.add_document(id=i, titulo=tit, fecha_publicacion=fec,
                            generos=gen, puntuaciones=pun)
        peliculas_i += 1

    writer.commit()

    tkMessageBox.showinfo("Indexar", "Se han indexado {} Peliculas".format(peliculas_i))
    
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
    
    for indice in range(1):
        pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/mejores/nota-espectadores/?page="+str(indice+1))
        print "http://www.sensacine.com/peliculas/mejores/nota-espectadores/?page="+str(indice+1)
        soup = BeautifulSoup(pagina, 'html.parser')
        
        link_pel="http://www.sensacine.com"
        all_links = soup.find_all(class_='no_underline')
        for l in all_links:
            link = link_pel + l.get('href')
            links.append(link)
        
    for e in links:
        pagina = urllib2.urlopen(e)
        print e
        soup = BeautifulSoup(pagina, 'html.parser')
        #Recogida de ID
            
        href = soup.find(class_='home item current').get('href').split('/')
        id_compl = href[2].split('-')
        ide = id_compl[1]
                  
        #Recogida de titulo
        titulo = soup.find('div',class_='titlebar-title').text
        u' '.join(titulo).encode('utf-8').strip()
            
        div= soup.find_all('div',class_='meta-body-item')
            
        #Comprobar si tiene fecha de re-estreno porque asi los divs son distintos
        i=0
        if soup.find(class_='meta-body-item').span.text == "Fecha de re-estreno":
            i=1
        #Recogida de fecha
        fecha = div[0+i].find(class_='date').text
                
        #Recogida de Genero
        list_gen = []
        gene= ""
        generos = div[3+i].find_all(class_='blue-link')
        for g in generos:
            gene+=g.text+","
            list_gen.append(g.text)  
        u' '.join(gene).encode('utf-8').strip()
        
        #Recogida de Directores   DA ERRORES AQUI NO PILLA DOS DIRECTORES
        list_direc =[]
        dire=""
        directores = div[i+1].find_all(itemprop='director')
        for d in directores:
            dire+=d.text+","
            list_direc.append(d.a.text)
        u' '.join(dire).encode('utf-8').strip()   
        #Recogida de Reparto
        rep=""
        reparto = div[2+i].find_all('span')
        actores= reparto[1:len(reparto)-1]
        for a in actores:
            rep+=a.text+","
                    
        #rep+=" y más".encode('utf-8').strip()
        u' '.join(rep).encode('utf-8').strip()  
         
        #Recogida de Synopsis
        synopsis = soup.find(class_='synopsis-txt').text.strip()
        u' '.join(synopsis).encode('utf-8').strip()
        
            #Recogida de votos
        votos = soup.find_all(class_='rating-item')
        votos_usuarios = ""
        votos_medios = ""
        votos_sensacine = ""
        for voto in votos:
            puntuacion =  voto.find(class_='rating-title').text.strip()
            if puntuacion == "Usuarios":
                votos_usuarios = voto.find(class_='stareval-note').text.strip()          
                               
            elif puntuacion == "Medios":
                votos_medios = voto.find(class_='stareval-note').text.strip()
                    
            elif puntuacion == "Sensacine":
                votos_sensacine = voto.find(class_='stareval-note').text.strip()
                    
    
        #datos.append((ide,titulo, list_direc, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine,list_gen ))
        #datos.append((ide,titulo, dire, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine ,list_direc))
        print (ide,titulo, dire, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine , gene)
        print synopsis
        row = str(ide+'|'+titulo+'|'+dire+'|'+rep+'|'+ synopsis+'|'+fecha+'|'+votos_usuarios+'|'+ votos_medios+'|'+ votos_sensacine+'|'+gene)
        csvsalida = open(ruta+'films.csv', 'w')
        salida = csv.writer(csvsalida)
        salida.writerow(row)
        del salida
        csvsalida.close()
    
    print "---------------------------------------------------"
    '''todo = np.asarray(datos)
    np.savetxt(ruta+'films.csv',   # Archivo de salida
           todo,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter="|")  
    
    '''
    

def crearUsuarios():
    e='adios'
    l='hola'
    palabra=[[l,e]]
    datos = np.asarray(palabra)
    np.savetxt(ruta+"users.csv",   # Archivo de salida
           datos,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter=",")

def crearPuntuaciones():
    e='adios'
    l='hola'
    #palabra=[[l,e],[e,l]]
    palabra =[]
    palabra.append([l,e])
    palabra.append([e,l])
    datos = np.asarray(palabra)
    np.savetxt(ruta+"ratings.csv",   # Archivo de salida
           datos,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter=",")
    
def crearGeneros():
    genres = []
    pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/mejores/nota-espectadores/")
    soup = BeautifulSoup(pagina, 'html.parser')
    
    columna = soup.find('div',class_='left_col_menu_item')

    generos = columna.find_all('li')[1:]
    for g in generos:
        genero = g.text.split('(')[0]
        gen =u' '.join(genero).encode('utf-8').strip()
        genres.append([gen])
    print len(genres)
    datos = np.asarray(genres)
    np.savetxt(ruta+"genres.csv",   # Archivo de salida
           datos,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter=",")

def crearCSV(request):
    crearPelis()
    #crearUsuarios()
    #crearPuntuaciones()
    #crearGeneros()
    return render_to_response('index.html')
    
def searchByGenre(request):
    if request.method=='GET':
        form = GenreForm(request.GET, request.FILES)
        peliculas=[]
        if form.is_valid():
            gen = form.cleaned_data['genre']
            genre = get_object_or_404(Genre, pk=gen) 
            ix = open_dir(dirindex)
            with ix.searcher() as searcher:
                query = QueryParser("genre", ix.schema).parse(unicode(genre))
                results = searcher.search(query)
                for r in results:
                    print r             
                    peliculas.append(r)
                    ##Buscar peliculas segun el Genero (Podria hacerse con Indices de Whoosh)
                    return render_to_response('films_by_genre.html', {'genre':genre},{'peliculas':peliculas})
    else:
        form=GenreForm()
    return render_to_response('search_genre.html', {'form':form }, context_instance=RequestContext(request))

def searchByUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            usuario = get_object_or_404(User, pk=idUser)
            return render_to_response('ratedFilms.html', {'usuario':usuario})
    else:
        form=UserForm()
    return render_to_response('search_user.html', {'form':form }, context_instance=RequestContext(request))

#Recomienda dos peliculas a un usuario que no haya puntuado
def recommendedFilms(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(User, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:2]
            items = []
            for re in recommended:
                item = Film.objects.get(pk=re[1])
                items.append(item)
            return render_to_response('recommendationItems.html', {'user': user, 'items': items}, context_instance=RequestContext(request))
    form = UserForm()
    return render_to_response('search_user.html', {'form': form}, context_instance=RequestContext(request))

#Recomienda 3 peliculas similares a la dada
def similarFilms(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            items=[]
            for re in recommended:
                print re
                print re[1]
                item = Film.objects.get(pk=int(re[1]))
                items.append(item)
            return render_to_response('similarFilms.html', {'film': film,'films': items}, context_instance=RequestContext(request))
    form = FilmForm()
    return render_to_response('search_film.html', {'form': form}, context_instance=RequestContext(request))

