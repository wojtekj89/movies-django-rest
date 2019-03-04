import requests
from core import settings

def get_movie(title):
    """Getting movie details from OMDB API"""
    params = {
        't': title,
        'apikey': settings.OMDB_API_KEY
    }

    r = requests.get(settings.OMDB_URL, params=params)
    response = r.json()

    return response