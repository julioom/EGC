from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator

# Create your models here.

class Occupation(models.Model):
    occupationName = models.CharField(max_length=30)
    def __unicode__(self):
        return unicode(self.occupationName)
            
class Genre(models.Model):
    genreName = models.CharField(max_length=20) 
    def __unicode__(self):
        return unicode(self.genreName)  
        
class User(models.Model):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(max_length=1, choices=(('F', 'Female'),('M','Male'),))
    occupation = models.ForeignKey(Occupation, on_delete=models.DO_NOTHING)
    def __unicode__(self):
        return unicode(self.gender+self.age)
    
        
class Film(models.Model):
    movieTitle = models.CharField(max_length=100)
    releaseDate = models.DateField(null=True, blank=True)
    releaseVideoDate = models.DateField(null=True, blank=True)
    IMDbURL = models.URLField(validators=[URLValidator()])
    genres = models.ManyToManyField(Genre)
    ratings = models.ManyToManyField(User, through='Rating')
    def __unicode__(self):
        return unicode(self.movieTitle)
    
    
class Rating(models.Model):
    user = models.ForeignKey(User)
    film = models.ForeignKey(Film)
    rateDate = models.DateField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
