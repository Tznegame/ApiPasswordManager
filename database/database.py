import mysql.connector
from mysql.connector import errorcode

class Database:

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(user='root', password='Massifi_1995',
                                          host='127.0.0.1',
                                          database='passwordmanager')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def aggiungiRecord(self, dati):
        cursor = self.cnx.cursor()
        self.cnx.commit()
        add_website = ("INSERT INTO website "
                       "(name, user, password) "
                       "VALUES (%s, %s, %s)")
        cursor.execute(add_website, dati)
        self.cnx.commit()
        cursor.close()

    def recuperaDati(self, website):
        cursor = self.cnx.cursor()
        select_stmt = """SELECT * FROM website WHERE name = %s"""
        cursor.execute(select_stmt, (website,))
        data = cursor.fetchone()
        cursor.close()
        return data

    def modificaRecord(self, dati):
        cursor = self.cnx.cursor()
        sql_update_query = """Update website set user = %s, password = %s where name = %s"""
        cursor.execute(sql_update_query, dati)
        cursor.close()

    def eliminaRecord(self, website):
        cursor = self.cnx.cursor()
        sql_update_query = """DELETE FROM website WHERE name = %s"""
        cursor.execute(sql_update_query, (website,))
        self.cnx.commit()
        cursor.close()