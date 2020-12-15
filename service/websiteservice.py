import json
import sys
from mysql.connector import errorcode
sys.path.append('C:/Development/ApiPasswordManager/api/model')
sys.path.append('C:/Development/ApiPasswordManager/api/security')
from security.security import Security
from model.website import Website
from database.database import Database
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import HTTPException, NotFound, BadRequest

class WebsiteService:

    def __init__(self):
        self.security = Security()
        self.database = Database()

    def aggiungiRecord(self, request_body):
        if not request_body['website'] or not request_body['usr'] or not request_body['psw']:
            raise BadRequest
        website = request_body['website']
        username = self.security.encrypt(request_body['usr'], self.security.key)
        password = self.security.encrypt(request_body['psw'], self.security.key)
        dati = (website, username, password)
        self.database.aggiungiRecord(dati)
        return "ok", 201


    def recuperaDati(self,  website):
        return self.database.recuperaDati(website)

    def visualizzaDati(self, query_parameters):
        if not query_parameters.get('website'):
            raise BadRequest
        data = self.recuperaDati(query_parameters.get('website'))
        website = Website(data[0], self.security.decrypt(data[1], self.security.key),
                          self.security.decrypt(data[2], self.security.key))
        
        return json.dumps(website.__dict__), 200

    def modificaRecord(self, request_body):
        if not request_body['website'] or not request_body['usr'] or not request_body['psw']:
            raise BadRequest
        name = self.recuperaDati(request_body['website'])[0]
        if name:
            user = request_body['usr']
            psw = request_body['psw']
            dati = (self.security.encrypt(user, self.security.key), self.security.encrypt(psw, self.security.key), name)
            self.database.modificaRecord(dati)
            return "ok", 202
        else:
            return "no"

    def eliminaRecord(self, request_body):
        if not request_body['website']:
            raise BadRequest
        name = self.recuperaDati(request_body['website'])[0]
        if name:
            self.database.eliminaRecord(name)
            return "ok", 204
        else:
            return "no"

    def handleException(self, e):
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
