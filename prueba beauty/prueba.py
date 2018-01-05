# encoding: UTF-8
import urllib2
from bs4 import BeautifulSoup

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
        

if __name__ == "__main__":
    cargar_datos()
    #cargar_generos()
    
    