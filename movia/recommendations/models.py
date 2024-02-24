from django.db import models
from users.models import CustomUser


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class ProductionCompany(models.Model):
    id = models.IntegerField(primary_key=True)
    logo_path = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=2)

class ProductionCountry(models.Model):
    iso_3166_1 = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255)

class SpokenLanguage(models.Model):
    iso_639_1 = models.CharField(max_length=2, primary_key=True)
    english_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=255, null=True)
    budget = models.IntegerField()
    homepage = models.URLField(null=True)
    imdb_id = models.CharField(max_length=255)
    original_language = models.CharField(max_length=2)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=255, null=True)
    release_date = models.DateField()
    revenue = models.IntegerField()
    runtime = models.IntegerField(null=True)
    status = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

    # Relations
    genres = models.ManyToManyField(Genre)
    production_companies = models.ManyToManyField(ProductionCompany)
    production_countries = models.ManyToManyField(ProductionCountry)
    spoken_languages = models.ManyToManyField(SpokenLanguage)
    # Ajoutez d'autres champs en fonction de vos besoins

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Ajoutez d'autres champs en fonction de vos besoins
    
class Serie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()