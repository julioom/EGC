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
            directores = pelicula.find(class_='meta-body-item meta-body-direction light').find_all('a')
            director = ""
            print ( directores )
            print ("/br")
            for i in directores:
                director = director + " , " + i.text
                print(director + "/br")
            
            
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
            print (datos)
            

       #pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/en-cartelera/cines/" + '?page=' + str(indice + 2))
        
        
    return datos


if __name__ == "__main__":
    cargar_datos()
    
    