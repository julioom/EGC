from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from pattern.db import primary_key


# Create your models here.

class Genre(models.Model):
    genreName = models.CharField(primary_key=True, max_length=20) 
    def __unicode__(self):
        return unicode(self.genreName)  
        
class User(models.Model):
    idUser = models.CharField(primary_key=True, max_length=20)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(max_length=1, choices=(('F', 'Female'), ('M', 'Male'),))
    def __unicode__(self):
        return unicode(self.gender + self.age)
    
        
class Film(models.Model):
    movieTitle = models.CharField(primary_key=True,max_length=1000)
    director = models.CharField(max_length=20)
    director = models.CharField(max_length=50)
    synopsis = models.CharField(max_length=1000)
    valorn_medios = models.DecimalField(max_digits=2,decimal_places=1)
    valor_usuarios = models.DecimalField(max_digits=2,decimal_places=1)
    valor_sensacine = models.DecimalField(max_digits=2,decimal_places=1)
    genres = models.ManyToManyField(Genre)
    ratings = models.ManyToManyField(User, through='Rating')
    def __unicode__(self):
        return unicode(self.movieTitle)    
    
class Rating(models.Model):
    user = models.ForeignKey(User)
    film = models.ForeignKey(Film)
    rateDate = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
