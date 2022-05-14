from flask_restful import Resource


class Artist(Resource):
    def get(self):
        return {'message': ''}
