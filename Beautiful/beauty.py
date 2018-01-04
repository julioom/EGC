def cargar_datos():
    datos = []
    usuarios = []

    pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/en-cartelera/cines/")

    for indice in range(5):

        soup = BeautifulSoup(pagina, 'html.parser')

        for pelicula in soup.find_all('div', class_='card card-entity card-entity-list cf'):
            titulo = pelicula.find(class_='meta-title').a.text
            genero = pelicula.find(class_='meta-body-item meta-body-info').find_all('a')[1].text
            director = pelicula.find(class_='meta-body-item meta-body-direction light').find_all('a')[1].text
            reparto = pelicula.find(class_='meta-body-item meta-body-actor light').find_all('a')[1].text
            synopsis = pelicula.find(class_='synopsis').text
            votos = pelicula.find_all(class_='rating-item')
            for voto in votos:
                puntuacion =  pelicula.find(class_='xXx rating-title blue-link').a.text
                if puntuacion == "USUARIOS":
                    votos_usuarios = voto.find(class_='stareval-note').txt                   
                    
                else if puntuacion == "MEDIOS":
                    votos_medios = voto.find(class_='stareval-note').txt
                else:
                    votos_sensacine = voto.find(class_='stareval-note').txt
                
           
            
            
            
            datos.append((titulo, genero, director, reparto, synopsis,votos_usuarios, votos_medios, votos_sensacine ))
            
            

        pagina = urllib2.urlopen("http://www.sensacine.com/peliculas/en-cartelera/cines/" + '?page=' + str(indice + 2))
        print (datos)
        
    return datos


if __name__ == "__main__":
    cargar_datos()
    
    
    
    
    