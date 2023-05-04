#import sqlite3
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

class PlacesDB():
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

    def createPlacesTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS places (id SERIAL PRIMARY KEY, city TEXT, state TEXT, country TEXT, activity TEXT, language TEXT, climate TEXT)")
        self.connection.commit()

    def getAllPlaces(self):
        self.cursor.execute("SELECT * FROM places")
        places = self.cursor.fetchall()
        return places
    
    def getOnePlace(self, place_id):
        data = [place_id]
        self.cursor.execute("SELECT * FROM places WHERE id = %s", data)
        place = self.cursor.fetchone()
        return place
    
    def deletePlace(self, place_id):
        data = [place_id]
        self.cursor.execute("DELETE FROM places WHERE id = %s", data)
        self.connection.commit()

    def createPlace(self, city, state, country, activity, language, climate):
        data = [city, state, country, activity, language, climate] 
        self.cursor.execute("INSERT INTO places (city, state, country, activity, language, climate) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.connection.commit()
    
    
    def updatePlace(self, member_id, city, state, country, activity, language, climate):
        data = [city, state, country, activity, language, climate, member_id] 
        self.cursor.execute("UPDATE places SET city = %s,  state = %s, country = %s, activity = %s, language= %s, climate = %s WHERE id = %s", data)
        self.connection.commit()
'''
connection = sqlite3.connect("places.db")
cursor = connection.cursor()

cursor.execute("INSERT INTO places (city, state, country, activity, language, climate) VALUES ('San Diego', 'California', 'US', 'surf', 'English', 'Mediterranean')")
connection.commit()


cursor.execute("SELECT * FROM places")
data = cursor.fetchall()
print(data)

'''