from models import *
from datetime import datetime
from django.db.transaction import commit_on_success

path = "Cine\\csv"

@commit_on_success
def populateOccupations():
    print("Loading occupations...")
    Occupation.objects.all().delete()
    
    fileobj=open(path+"\\u.occupation", "r")
    line=fileobj.readline()
    while line:
        occ = line.strip().decode('utf-8', 'replace')
        if len(occ)>0:
            Occupation.objects.create(occupationName=occ)
        line=fileobj.readline()
    fileobj.close()
    
    print("Occupations inserted: " + str(Occupation.objects.count()))
    print("---------------------------------------------------------")
    
    
@commit_on_success
def populateGenres():
    print("Loading Movie Genres...")
    Genre.objects.all().delete()
    
    fileobj=open(path+"\\u.genre", "r")
    line=fileobj.readline()
    while line:
        id_gen = line.split('|')
        if len(id_gen)>1:
            gen = id_gen[0].strip().decode('utf-8', 'replace')
            ide = int(id_gen[1].strip())
            Genre.objects.create(id=ide,genreName=gen)
        line=fileobj.readline()
    fileobj.close()
    
    print("Genres inserted: " + str(Genre.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateUsers():
    print("Loading users...")
    User.objects.all().delete()
    
    fileobj=open(path+"\\u.user", "r")
    line=fileobj.readline()
    while line:
        data = line.split('|')
        if len(data)>1:
            ide = int(data[0].strip())
            ag = int(data[1].strip())
            gen = data[2].strip()
            ocu = data[3].strip().decode('utf-8', 'replace')
            zc = data[4].strip()
            User.objects.create(id=ide, age=ag, gender=gen, occupation=Occupation.objects.get(occupationName=ocu), zipCode=zc)   
        line=fileobj.readline()
    fileobj.close()
    
    print("Users inserted: " + str(User.objects.count()))
    print("---------------------------------------------------------")


@commit_on_success
def populateFilms():
    print("Loading movies...")
    Film.objects.all().delete()
    
    fileobj=open(path+"\\u.item", "r")
    line=fileobj.readline()
    while line:
        data = line.split('|')
        if len(data)>1:
            ide = int(data[0].strip())
            tit = data[1].strip().decode('utf-8', 'replace')
            try:
                date_rel = datetime.strptime(data[2].strip(),'%d-%b-%Y')
            except:
                date_rel = datetime.strptime('01-Jan-1900','%d-%b-%Y')
            try:
                date_rel_video = datetime.strptime(data[3].strip(),'%d-%b-%Y')
            except:
                date_rel_video = date_rel
            i_url = data[4].strip().decode('utf-8', 'replace')
            list_genres =[]
            for i in range(19):
                if data[5+i].strip() == '1':
                    list_genres.append(i)
            movie = Film.objects.create(id=ide, movieTitle=tit, releaseDate=date_rel, releaseVideoDate=date_rel_video, IMDbURL=i_url)
            for c in list_genres:
                movie.genres.add(Genre.objects.get(id=c))    

        line=fileobj.readline()
    fileobj.close()
    
    print("Movies inserted: " + str(Film.objects.count()))
    print("---------------------------------------------------------")

       
@commit_on_success
def populateRatings():
    print("Loading ratings...")
    Rating.objects.all().delete()

    fileobj=open(path+"\\u.data", "r") #rb
    line=fileobj.readline()
    i=0
    while line:
        data = line.split('\t')
        if len(data)>1:
            fil = Film.objects.get(id = int(data[1].strip()))
            use = User.objects.get(id = int(data[0].strip()))
            rat = int(data[2].strip())
            dat = datetime.fromtimestamp(int(data[3].strip()))   
            Rating.objects.create(user=use, film=fil, rateDate=dat, rating=rat)
            i=i+1
            if i%10000 == 0:
                print(str(i) + " ratings have been saved...")
        line=fileobj.readline()
    fileobj.close()
       
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    populateOccupations()
    populateGenres()
    populateUsers()
    populateFilms()
    populateRatings()
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()
    
