import requests
from unidecode import unidecode


BASE_URL = "https://api.genius.com"

class Genius:

    def __init__(self, token):
        self.token = token

    def _get(self, path, params=None, headers=None):
        requrl = '/'.join([BASE_URL, path])
        token = "Bearer {}".format(self.token)
        if headers:
            headers['Authorization'] = token
        else:
            headers = {"Authorization": token}

        response = requests.get(url=requrl, params=params, headers=headers)
        response.raise_for_status()

        return response.json()


    def get_artist_id_by_name(self, artist_name):
        artist_name = self.clean_name(artist_name)
        data = self._get("search", {'q': artist_name})

        artist_id = None
        for hit in data["response"]["hits"]:
            hit_name = self.clean_name(hit["result"]["primary_artist"]["name"])
            if hit_name == artist_name:
                artist_id = hit["result"]["primary_artist"]["id"]
                break

        return artist_id

    def get_artist_songs(self, artist_id):
        current_page = 1
        next_page = True
        songs = []

        while len(songs) < 10 and next_page:

            path = "artists/{}/songs/".format(artist_id)
            params = {'page': current_page, 'sort': 'popularity'}
            data = self._get(path=path, params=params)

            page_songs = data['response']['songs']

            if page_songs:
                singer_songs = [song['title'] for song in page_songs
                if song["primary_artist"]["id"] == artist_id]

                songs += singer_songs
                current_page += 1
            else:
                next_page = False

        return songs[:10]

    def clean_name(self, artist_name):
        return unidecode(artist_name.strip().lower().title())
