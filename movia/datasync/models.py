import os

import requests
from django.db import models
from dotenv import load_dotenv
from recommendations.models import (Genre, Movie, ProductionCompany,
                                    ProductionCountry, Serie, SpokenLanguage)

load_dotenv(dotenv_path='.env.local')

def get_content_info(content_id, content_type):
    """
    Retrieves information about a movie from The Movie Database (TMDB) API.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        dict: A dictionary containing the movie information.

    Raises:
        None
    """
    api_key = os.getenv('TMDB_API_KEY')
    response = requests.get(f'https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={api_key}&language=fr-FR')
    # Vérifier que la requête a réussi
    if response.status_code == 200:
        data = response.json()
    return data


def update_database_with_movie(movie_data):
    """
    Met à jour la base de données avec les informations d'un film.

    Args:
        movie_data (dict): Les données du film à mettre à jour.

    Returns:
        tuple: Un tuple contenant l'objet Movie mis à jour et un booléen indiquant si le film a été créé ou non.
    """
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

def update_database_with_serie(series_data):
    # Récupérer ou créer la série
    serie, created = Serie.objects.get_or_create(id=series_data['id'], defaults={
        'backdrop_path': series_data['backdrop_path'],
        'homepage': series_data['homepage'],
        'original_language': series_data['original_language'],
        'original_title': series_data['original_name'],
        'overview': series_data['overview'],
        'popularity': series_data['popularity'],
        'poster_path': series_data['poster_path'],
        'release_date': series_data['first_air_date'],
        'status': series_data['status'],
        'title': series_data['name'],
        'vote_average': series_data['vote_average'],
        'vote_count': series_data['vote_count'],
    })

    # Si la série a été créée, ajouter les relations
    if created:
        for genre_data in series_data['genres']:
            genre, _ = Genre.objects.get_or_create(id=genre_data['id'], defaults={'name': genre_data['name']})
            serie.genres.add(genre)

        for company_data in series_data['production_companies']:
            company, _ = ProductionCompany.objects.get_or_create(id=company_data['id'], defaults={'name': company_data['name']})
            serie.production_companies.add(company)

        for country_data in series_data['production_countries']:
            country, _ = ProductionCountry.objects.get_or_create(iso_3166_1=country_data['iso_3166_1'], defaults={'name': country_data['name']})
            serie.production_countries.add(country)

        for language_data in series_data['spoken_languages']:
            language, _ = SpokenLanguage.objects.get_or_create(iso_639_1=language_data['iso_639_1'], defaults={'name': language_data['name']})
            serie.spoken_languages.add(language)

        serie.save()
    
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
        movie_data = get_content_info(i, 'movie')
        serie_data = get_content_info(i, 'tv')
        update_database_with_movie(movie_data)
        update_database_with_serie(serie_data)

