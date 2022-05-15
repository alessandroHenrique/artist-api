from flask_restful import Resource
from common.database import ArtistDB


class Dynamo(Resource):
    
    def get(self):
        db = ArtistDB()
        db.create_table_artist()
        return {"message": "Table created"}
