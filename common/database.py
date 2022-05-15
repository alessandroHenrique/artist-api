import uuid
from boto3 import resource
from decouple import config


AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME = config("REGION_NAME")


class ArtistDB:
    def __init__(self):
        self.resource = resource(
            'dynamodb',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name = REGION_NAME
        )
        self.artist_table = self.resource.Table('Artist')

    def create_table_artist(self):   
        table = self.resource.create_table(
            TableName = 'Artist',
            KeySchema = [
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH' #RANGE = sort key, HASH = partition key
                }
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'name', # Name of the attribute
                    'AttributeType': 'S'   # S = String (B= Binary, S = String)
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits'  : 5,
                'WriteCapacityUnits': 5
            }
        )
        return table

    def create_artist(self, name, cache=True):
        id = str(uuid.uuid4())

        response = self.artist_table.put_item(
            Item = {
                'id': id,
                'name': name,
                'cache': cache
            }
        )
        return response

    def get_artist(self, name):
        response = self.artist_table.get_item(
            Key = {
                'name': name
            }
        )
        return response.get('Item', None)

    def update_artist_cache(self, name, cache):
        response = self.artist_table.update_item(
            Key = {
                'name': name
            },
            AttributeUpdates={
                'cache': {
                    'Value'  : cache,
                    'Action' : 'PUT'
                }
            },

            ReturnValues = "UPDATED_NEW"  # returns the new updated values
        )

        return response
