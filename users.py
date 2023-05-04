#import sqlite3
from passlib.hash import bcrypt
import os
import psycopg2
import psycopg2.extras
import urllib.parse

'''
def dict_factory(cursor, row):
    d ={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
'''
class UsersDB():
    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, last TEXT, email TEXT, password TEXT)")
        self.connection.commit()

    def createUser(self, firstname, lastname, aemail, apassword):
        h = bcrypt.hash(apassword)
        data = [firstname, lastname, aemail, h] 
        self.cursor.execute("INSERT INTO users (name, last, email, password) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()
    
    def validateEmail(self, aemail):
        data = [aemail]
        self.cursor.execute("SELECT * FROM users WHERE email = %s", data)
        email = self.cursor.fetchone()
        return email

    def validatePassword(self, apassword, aemail):
        data = [aemail]
        self.cursor.execute("SELECT password FROM users WHERE email = %s", data)
        password = self.cursor.fetchone()
        return bcrypt.verify(apassword, password['password'])

    def getUser(self, aemail):
        data = [aemail]
        self.cursor.execute("SELECT id FROM users WHERE email = %s", data)
        userId = self.cursor.fetchone()
        return userId