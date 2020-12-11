
import mysql.connector
import json
import sys
from mysql.connector import errorcode
sys.path.append('C:/Development/ApiPasswordManager/api/model')
sys.path.append('C:/Development/ApiPasswordManager/api/security')
from security.security import Security
from model.website import Website

class WebsiteService:

    def __init__(self, name):
        self.name = name
        self.security = Security(name)

    def checkInput(self, functionParam, userInput, testo):
        if len(userInput) != 0:
            return userInput
        else:
            return functionParam(testo)

    def inserimentoDati(self,testo):
        userInput = str(input(testo + "\n"))
        return self.checkInput(self.inserimentoDati, userInput, testo)

    def aggiungiRecord(self, cnx, key, request_body):
        cursor = cnx.cursor()
        website = request_body['website']
        username = self.security.encrypt(request_body['usr'], key)
        password = self.security.encrypt(request_body['psw'], key)
        dati = (website, username, password)
        add_website = ("INSERT INTO website "
            "(name, user, password) "
            "VALUES (%s, %s, %s)")
        cursor.execute(add_website, dati)
        cnx.commit()
        cursor.close()
        return "ok", 201


    def recuperaDati(self, cnx, website):
        cursor = cnx.cursor()
        select_stmt = """SELECT * FROM website WHERE name = %s"""
        cursor.execute(select_stmt, (website,))
        data = cursor.fetchone()
        cursor.close()
        return data

    def visualizzaDati(self, cnx, key, query_parameters):
        data = self.recuperaDati(cnx, query_parameters.get('website'))
        website = Website(data[0], self.security.decrypt(data[1], key), self.security.decrypt(data[2], key))
        
        return json.dumps(website.__dict__)

    def modificaRecord(self, cnx, key, request_body):
        name = self.recuperaDati(cnx, request_body['website'])[0]
        if name:
            cursor = cnx.cursor()
            user = request_body['usr']
            psw = request_body['psw']
            sql_update_query = """Update website set user = %s, password = %s where name = %s"""
            dati = (self.security.encrypt(user, key), self.security.encrypt(psw, key), name)
            cursor.execute(sql_update_query, dati)
            cursor.close()
            return "ok"
        else:
            return "no"

    def eliminaRecord(self, cnx, key, request_body):
        name = self.recuperaDati(cnx, request_body['website'])[0]
        if name:
            cursor = cnx.cursor()
            sql_update_query = """DELETE FROM website WHERE name = %s"""
            cursor.execute(sql_update_query, (name,))
            cnx.commit()
            cursor.close()
            return "ok"
        else:
            return "no"

    def recuperaChiave(self):
        psw = self.security.checkPassword(input("Inserisci la password \n"))
        key = self.security.recoverKey(psw)
        print("key: " + key.decode('utf-8'))
        return key

    def api_startup(self):
        # connection to DB
        try:
            cnx = mysql.connector.connect(user='root', password='Massifi_1995',
                                        host='127.0.0.1',
                                        database='passwordmanager')
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)