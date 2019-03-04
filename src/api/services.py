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

    if not r.ok:
        raise requests.exceptions(r.status_code, 'OMDB API error')

    else:
        response = r.json()
        if response['Response'] == 'False':
            """ When OMDB API can't find a movie status code is 200 """
            raise (requests.exceptions.HTTPError(404, response['Error']))
        else:
            return response