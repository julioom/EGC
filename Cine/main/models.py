from django.db import models
from pattern.db import primary_key


# Create your models here.

class Genre(models.Model):
    genreName = models.CharField(primary_key=True,max_length=20) 
    def __unicode__(self):
        return unicode(self.genreName)  
        
class User(models.Model):
    idUser = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return unicode(self.name)
    
        
class Film(models.Model):
    idMovie = models.BigIntegerField(primary_key=True)
    movieTitle = models.CharField(max_length=1000)
    director = models.CharField(max_length=20)
    reparto = models.CharField(max_length=50)
    synopsis = models.CharField(max_length=1000)
    releaseDate = models.CharField(null=True, blank=True,max_length=30)
    url = models.URLField(verify_exists=True,max_length=200)
    valor_medios = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    valor_usuarios = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    valor_sensacine = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    genres = models.ManyToManyField(Genre)
    ratings = models.ManyToManyField(User, through='Rating')
    def __unicode__(self):
        return unicode(self.movieTitle)    
    
class Rating(models.Model):
    user = models.ForeignKey(User)
    film = models.ForeignKey(Film)
    rateDate = models.DateField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    def __unicode__(self):
        return unicode(self.user+self.film+self.rating) 