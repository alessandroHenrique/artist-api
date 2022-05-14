from flask import request, abort
from flask_restful import Resource
from ..common.database import Artist


db = Artist()

class Artist(Resource):
    def get(self):
        name = request.args.get('q', None)
        artist = db.get_artist(name)
        if artist:
            return artist
        else:
            response = db.create_artist(name)
            if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
                return {
                    'success': True,
                    'msg': 'Added successfully',
                }
            abort(400)
