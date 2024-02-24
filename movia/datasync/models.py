import os

import requests
from django.db import models
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local')

def get_movie_info(movie_id):
    api_key = os.getenv('TMDB_API_KEY')
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=fr-FR')
    data = response.json()
    return data

from recommendations.models import Movie


def update_database_with_movie(movie_data):
    Movie.objects.create(
        title=movie_data['title'],
        description=movie_data['overview'],
        # Ajoutez d'autres champs ici
    )
    
def update_database_with_tmdb_info():
    for movie_id in range(1, 100):  # Remplacez cette plage par la plage de IDs de films que vous voulez récupérer
        movie_data = get_movie_info(movie_id)
        update_database_with_movie(movie_data)