# encoding: UTF-8

import urllib2
from bs4 import BeautifulSoup
import numpy as np
import csv, operator

ruta="prueba beauty\\csv\\"

def cargar_datos():
    datos = []
   

    pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/en-cartelera/cines/")

    #for indice in range(5):

    soup = BeautifulSoup(pagina, 'html.parser')

    for pelicula in soup.find_all('div', class_='card card-entity card-entity-list cf'):
          
            #Recogida de titulo
            titulo = pelicula.find(class_='meta-title').a.text
            
            #Recogida de Genero
            genero = pelicula.find(class_='meta-body-item meta-body-info').find_all('a')
            
            #Recogida de Directores   DA ERRORES AQUI NO PILLA DOS DIRECTORES
            #directores = pelicula.find(class_='meta-body-item meta-body-direction light').find_all('a')
            directores = pelicula.find(class_='meta-body-item meta-body-direction light').text.strip()
            x = directores.split("\n")
            director=""
            print(x[1])
            '''if x[2] is not None:
                print x[2]'''
            '''for i in x:
                print i+"31234465241\n"
                y= i.split("\n")
                
                if len(y)==1:
                    print y[0]
                elif len(y)==2:
                    print y'''
                #director = i.text
                #print(y)
            
            
            #Recogida de Reparto
            reparto = pelicula.find(class_='meta-body-item meta-body-actor light').find_all('a')
            
            #Recogida de Synopsis
            synopsis = pelicula.find(class_='synopsis').text
            
            #Recogida de votos
            votos = pelicula.find_all(class_='rating-item')
            for voto in votos:
                puntuacion =  voto.a
                votos_usuarios = None
                votos_medios = None
                votos_sensacine = None
                
                if puntuacion == "USUARIOS":
                    votos_usuarios = voto.a                 
                    
                elif puntuacion == "MEDIOS":
                    votos_medios = voto.a
                else:
                    votos_sensacine = voto.a
                
           
            
            
            
            datos.append((titulo, genero, director, reparto, synopsis,votos_usuarios, votos_medios, votos_sensacine ))
            #print (datos)
            

       #pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/en-cartelera/cines/" + '?page=' + str(indice + 2))
        
        
    return datos

def cargar_generos():
    datos = []
    pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/mejores/nota-espectadores/")
    soup = BeautifulSoup(pagina, 'html.parser')
    
    columna = soup.find('div',class_='left_col_menu_item')

    generos = columna.find_all('li')[1:]
    for g in generos:
        genero = g.text.split()[0]
        print genero
        
def cargar_datos2():
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
        id = id_compl[1]
                  
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
                    
    
        #datos.append((titulo, list_gen, list_direc, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine ))
        #datos.append((titulo, gene, dire, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine ))
        print (titulo, gene, dire, rep, synopsis,fecha,votos_usuarios, votos_medios, votos_sensacine )
        print synopsis
        row = str(titulo+"|"+gene+'|'+dire+'|'+rep+'|'+ synopsis+'|'+fecha+'|'+votos_usuarios+'|'+ votos_medios+'|'+ votos_sensacine)
        row.encode('utf-8')
        csvsalida = open('C:\\Users\\JULIO\\eclipse-workspace\\prueba beauty\\csv\\films.csv', 'w')
        salida = csv.writer(csvsalida)
        salida.writerow(row)
        del salida
        csvsalida.close()
    
    print "---------------------------------------------------"
    '''todo = np.asarray(datos)
    np.savetxt('C:\\Users\\JULIO\\eclipse-workspace\\prueba beauty\\csv\\films.csv', #ruta+"films.csv",   # Archivo de salida
           todo,        # datos
           fmt="%s",       # Usamos strings (%d para enteros)
           delimiter="|")  
    
    '''
    

if __name__ == "__main__":
    cargar_datos2()
    #cargar_generos()
    
    