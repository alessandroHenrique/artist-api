from flask import request, abort
from flask_restful import Resource
from decouple import config
from ..common.database import Artist
from ..common.util import Genius


db = Artist()

class Artist(Resource):
    def get(self):
        name = request.args.get('q', None)

        # Caso name venha com conteúd
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
                    _ = db.create_artist(name)
                else:
                    # TODO: checar cache do redis
                    pass

                songs = genius_api.get_artist_songs(id)
            else:
                abort(404, "Artist not found")

            # Caso o artista tenha músicas
            if len(songs) > 0:
                return {"songs": songs}
            else:
                abort(404, "Artist has no songs")

        return abort(400, "Search term is not valid")
