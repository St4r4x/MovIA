from django.db import models
from users.models import CustomUser


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Ajoutez d'autres champs en fonction de vos besoins

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Ajoutez d'autres champs en fonction de vos besoins