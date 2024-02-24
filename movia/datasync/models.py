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

def get_tv_series_info(serie_id):
    api_key = os.getenv('TMDB_API_KEY')
    response = requests.get(f'https://api.themoviedb.org/3/tv/{serie_id}?api_key={api_key}&language=fr-FR')
    data = response.json()
    return data

from recommendations.models import (Genre, Movie, ProductionCompany,
                                    ProductionCountry, Serie, SpokenLanguage)


def update_database_with_movie(movie_data):
    # Créer les genres
    genres = [Genre.objects.get_or_create(id=genre_data['id'], defaults={'name': genre_data['name']})[0] for genre_data in movie_data['genres']]

    # Créer les compagnies de production
    production_companies = [ProductionCompany.objects.get_or_create(id=company_data['id'], defaults={'logo_path': company_data['logo_path'], 'name': company_data['name'], 'origin_country': company_data['origin_country']})[0] for company_data in movie_data['production_companies']]

    # Créer les pays de production
    production_countries = [ProductionCountry.objects.get_or_create(iso_3166_1=country_data['iso_3166_1'], defaults={'name': country_data['name']})[0] for country_data in movie_data['production_countries']]

    # Créer les langues parlées
    spoken_languages = [SpokenLanguage.objects.get_or_create(iso_639_1=language_data['iso_639_1'], defaults={'english_name': language_data['english_name'], 'name': language_data['name']})[0] for language_data in movie_data['spoken_languages']]

    # Créer le film
    movie, created = Movie.objects.get_or_create(
        id=movie_data['id'],
        defaults={
            'adult': movie_data['adult'],
            'backdrop_path': movie_data['backdrop_path'],
            'budget': movie_data['budget'],
            'homepage': movie_data['homepage'],
            'imdb_id': movie_data['imdb_id'],
            'original_language': movie_data['original_language'],
            'original_title': movie_data['original_title'],
            'overview': movie_data['overview'],
            'popularity': movie_data['popularity'],
            'poster_path': movie_data['poster_path'],
            'release_date': movie_data['release_date'],
            'revenue': movie_data['revenue'],
            'runtime': movie_data['runtime'],
            'status': movie_data['status'],
            'tagline': movie_data['tagline'],
            'title': movie_data['title'],
            'video': movie_data['video'],
            'vote_average': movie_data['vote_average'],
            'vote_count': movie_data['vote_count'],
        }
    )

    # Associer les genres, les compagnies de production, les pays de production et les langues parlées au film
    if created:
        movie.genres.set(genres)
        movie.production_companies.set(production_companies)
        movie.production_countries.set(production_countries)
        movie.spoken_languages.set(spoken_languages)

def update_database_with_serie(serie_data):
    Serie.objects.create(
        title=serie_data['title'],
        description=serie_data['overview'],
        # Ajoutez d'autres champs ici
    )
    
def update_database_with_tmdb_info():
    """
    Update the database with movie and TV series information from TMDB.

    This function retrieves movie and TV series information from TMDB
    using a range of IDs and updates the database with the retrieved data.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(1, 100):  # Remplacez cette plage par la plage de IDs de films que vous voulez récupérer
        movie_data = get_movie_info(i)
        serie_data = get_tv_series_info(i)
        update_database_with_movie(movie_data)
        update_database_with_serie(serie_data)

