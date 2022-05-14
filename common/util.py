import requests


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
                songs += page_songs
                current_page += 1
            else:
                next_page = False

        songs = [song['title'] for song in songs
                if song["primary_artist"]["id"] == artist_id]
        return songs
