from flask import request, abort
from flask_restful import Resource
from decouple import config
from common.database import ArtistDB
from common.util import Genius
from redis import Redis
import json


db = ArtistDB()
CACHE_REDIS_HOST = config("CACHE_REDIS_HOST")
CACHE_REDIS_PORT = config("CACHE_REDIS_PORT")

redis_client = Redis(CACHE_REDIS_HOST, CACHE_REDIS_PORT)


class Artist(Resource):

        def remove_songs_from_cache(self, name, artist_cache, request_cache):
            _ = db.update_artist_cache(name, request_cache)
            if artist_cache:
                redis_client.delete(name)

        def get_cached_songs(self, name):
            songs = json.loads(redis_client.get(name))
            return {"songs": songs}

        def get_songs_response(self, name, songs, request_cache):
            if len(songs) > 0:
                if request_cache:
                    json_songs = json.dumps(songs)
                    redis_client.set(name, json_songs, 604800)
                return {"songs": songs}
            else:
                abort(404, "Artist has no songs")

        def get_request_cache_value(self, request_cache):
            if type(request_cache) is str:
                truthy_values = {'true', 't'}
                false_values = {'false', 'f'}
                if request_cache.lower() in truthy_values:
                    request_cache = True
                elif request_cache.lower() in false_values or request_cache == '':
                    request_cache = False
                else:
                    abort(400, "Cache value not valid")

            return request_cache

        def get(self):
            name = request.args.get('q', None)
            request_cache = self.get_request_cache_value(request.args.get('cache', True))

            db = ArtistDB()

            # Caso name venha com conteúdo
            if name:
                token = config("CLIENT_ACCESS_TOKEN")
                genius_api = Genius(token)
                id = genius_api.get_artist_id_by_name(name)
                songs = []

                # Caso o artista exista
                if id:
                    artist = db.get_artist(name)

                    # Caso o artista exista mas não está no dynamo, adiciona
                    if not artist:
                        _ = db.create_artist(name, request_cache)
                    else:
                        artist_cache = artist['cache']

                        if not request_cache:
                            self.remove_songs_from_cache(name, artist_cache, request_cache)
                        else:
                            # Caso as músicas do artista estiverem cacheadas, retorna elas
                            if not artist_cache:
                                _ = db.update_artist_cache(name, True)
                            else:
                                return self.get_cached_songs(name)

                    songs = genius_api.get_artist_songs(id)
                else:
                    abort(404, "Artist not found")

                return self.get_songs_response(name, songs, request_cache)

            return abort(400, "Search term is not valid")
