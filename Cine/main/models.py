from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.

class Genre(models.Model):
    genreName = models.CharField(primary_key=True,max_length=20) 
    def __unicode__(self):
        return unicode(self.genreName)  
        
class User(models.Model):
    idUser=models.CharField(primary_key=True, max_length=20)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(max_length=1, choices=(('F', 'Female'),('M','Male'),))
    localization = models.CharField(max_length=40)
    def __unicode__(self):
        return unicode(self.gender+self.age)
    
        
class Film(models.Model):
    idFilm=models.CharField(primary_key=True, max_length=20)
    movieTitle = models.CharField(max_length=100)
    releaseDate = models.DateField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    ratings = models.ManyToManyField(User, through='Rating')
    def __unicode__(self):
        return unicode(self.movieTitle)
    
    
class Rating(models.Model):
    user = models.ForeignKey(User)
    film = models.ForeignKey(Film)
    rateDate = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
