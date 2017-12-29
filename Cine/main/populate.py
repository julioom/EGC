from models import Genre,User,Film,Rating
from datetime import datetime
from django.db.transaction import commit_on_success

path = "Cine\\csv"
    
@commit_on_success
def populateGenres():
    print("Loading Movie Genres...")
    Genre.objects.all().delete()
    
    fileobj=open(path+"\\genres.csv", "r")
    line=fileobj.readline()
    while line: #Cada linea es un genero
        gen = line.decode('utf-8', 'replace')
        Genre.objects.create(genreName=gen)
        line=fileobj.readline()
    fileobj.close()
    
    print("Genres inserted: " + str(Genre.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateUsers():
    print("Loading users...")
    User.objects.all().delete()
    
    fileobj=open(path+"\\users.csv", "r")
    line=fileobj.readline()
    while line:
        data = line.split(',')
        if len(data)>1:
            ide = data[0].strip()
            ag = int(data[1].strip())
            gen = data[2].strip()
            loc = data[3].strip()
            User.objects.create(idUser=ide, age=ag, gender=gen, localization=loc)   
        line=fileobj.readline()
    fileobj.close()
    
    print("Users inserted: " + str(User.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateFilms():
    print("Loading movies...")
    Film.objects.all().delete()
    
    fileobj=open(path+"\\films.csv", "r")
    line=fileobj.readline()
    while line:
        data = line.split(',')
        if len(data)>1:
            ide = data[0].strip()
            tit = data[1].strip().decode('utf-8', 'replace')
            try:
                date_rel = datetime.strptime(data[2].strip(),'%d-%b-%Y')
            except:
                date_rel = datetime.strptime('01-Jan-1900','%d-%b-%Y')
            list_genres =[]
            for i in range(29): #numero de generos
                if data[4+i].strip() != None:
                    list_genres.append(data[4+i].strip())
            Film.objects.create(idFilm=ide, movieTitle=tit, releaseDate=date_rel,genres=list_genres) 

        line=fileobj.readline()
    fileobj.close()
    
    print("Movies inserted: " + str(Film.objects.count()))
    print("---------------------------------------------------------")

       
@commit_on_success
def populateRatings():
    print("Loading ratings...")
    Rating.objects.all().delete()

    fileobj=open(path+"\\ratings.csv", "r") #rb
    line=fileobj.readline()
    i=0
    while line:
        data = line.split(',')
        if len(data)>1:
            use = User.objects.get(id = data[0].strip())
            fil = Film.objects.get(id = data[1].strip())
            dat = datetime.fromtimestamp(int(data[2].strip()))   
            rat = int(data[3].strip())
            Rating.objects.create(user=use, film=fil, rateDate=dat, rating=rat)
            i=i+1
            if i%10000 == 0:
                print(str(i) + " ratings have been saved...")
        line=fileobj.readline()
    fileobj.close()
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    populateGenres()
    populateUsers()
    populateFilms()
    populateRatings()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()
    
