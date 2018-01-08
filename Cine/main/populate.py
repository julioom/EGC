from models import Genre, User, Film, Rating
from datetime import datetime
from django.db.transaction import commit_on_success

path = "Cine\\csv"
    
@commit_on_success
def populateGenres():
    print("Loading Movie Genres...")
    Genre.objects.all().delete()
    
    fileobj = open(path + "\\genres.csv", "r")
    line = fileobj.readline()
    while line:  # Cada linea es un genero
        gen = line.decode('utf-8', 'replace')
        Genre.objects.create(genreName=gen)
        line = fileobj.readline()
    fileobj.close()
    
    print("Genres inserted: " + str(Genre.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateUsers():
    print("Loading users...")
    User.objects.all().delete()
    
    fileobj = open(path + "\\users.csv", "r")
    line = fileobj.readline()
    while line:
        data = line.split(',')
        if len(data) > 1:
            ide = data[0].strip()
            ag = int(data[1].strip())
            gen = data[2].strip()
            loc = data[3].strip()
            User.objects.create(idUser=ide, age=ag, gender=gen, localization=loc)   
        line = fileobj.readline()
    fileobj.close()
    
    print("Users inserted: " + str(User.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateFilms():
    print("Loading movies...")
    Film.objects.all().delete()
    
    fileobj = open(path + "\\films.csv", "r")
    line = fileobj.readline()
    while line:
        data = line.split('|')
        if len(data) > 1:
            ide = int(data[0].strip())
            tit = data[1].strip().decode('utf-8', 'replace')
            dir = data[2].strip().decode('utf-8', 'replace')
            rep = data[3].strip().decode('utf-8', 'replace')
            sin = data[4].strip().decode('utf-8', 'replace')
            med = int(data[6].strip())
            usu = int(data[7].strip())
            sen = int(data[8].strip())
            try:
                date_rel = datetime.strptime(data[4].strip(), '%d-%b-%Y')
            except:
                date_rel = datetime.strptime('01-Jan-1900', '%d-%b-%Y')
            list_genres = []
            if data[9].strip() != None:
                generos=data[9].split(',').strip()
                for g in generos:
                    list_genres.append(g)
            film = Film.objects.create(idMovie= ide,movieTitle=tit, director=dir, reparto=rep, synopsis=sin, releaseDate=date_rel, valor_medios=med, valor_usuarios=usu,
                                valor_sensacine=sen) 
            for c in list_genres:
                film.genres.add(Genre.objects.get(genreName=c))
                
        line = fileobj.readline()
    fileobj.close()
    
    print("Movies inserted: " + str(Film.objects.count()))
    print("---------------------------------------------------------")

       
@commit_on_success
def populateRatings():
    print("Loading ratings...")
    Rating.objects.all().delete()

    fileobj = open(path + "\\ratings.csv", "r")  # rb
    line = fileobj.readline()
    i = 0
    while line:
        data = line.split(',')
        if len(data) > 1:
            use = User.objects.get(id=data[0].strip())
            fil = Film.objects.get(id=data[1].strip())
            dat = datetime.fromtimestamp(int(data[2].strip()))   
            rat = int(data[3].strip())
            Rating.objects.create(user=use, film=fil, rateDate=dat, rating=rat)
            i = i + 1
            if i % 10000 == 0:
                print(str(i) + " ratings have been saved...")
        line = fileobj.readline()
    fileobj.close()
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    populateGenres()
    # populateUsers()
    # populateFilms()
    # populateRatings()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()
    
