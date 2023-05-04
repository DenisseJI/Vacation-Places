from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
#from dummydb import DummyDB
from places import PlacesDB
from users import UsersDB
from session_store import SessionStore
import json
import os.path
import sys

SESSION_STORE = SessionStore()
class MyRequestHandler(BaseHTTPRequestHandler):
    
    def load_cookie(self):
        print("let's see the request headers:", self.headers)
        
        #if request headers contain cookie data
        if "Cookie" in self.headers:
            # load cookie data from the request headers
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            #otherwis, create and empty cookie object
            self.cookie = cookies.SimpleCookie()   

    def send_cookie(self):
        # write response headers based on cookie data
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString()) 
    
    # load the session data that corresponds with the current client
    # save the session for the CURRENT client  into self.session
    def load_session(self):
        self.load_cookie()

        #check if session ID cookie exists
        if "sessionId" in self.cookie:
            #load session from session store using session ID
            sessionId = self.cookie["sessionId"].value
            self.sessionData = SESSION_STORE.getSessionData(sessionId)

            #if cannot load session(inavalise session ID)?
            if self.sessionData == None:
                #create a new session, with a new session ID
                sessionId = SESSION_STORE.createSession()
                #set the new session ID into the session ID cookie
                self.cookie["sessionId"] = sessionId
                #load the new sessino data
                self.sessionData = SESSION_STORE.getSessionData(sessionId)
        else:
            #create a new session, with a new session ID
            sessionId = SESSION_STORE.createSession()
            #set the new session ID into the session ID cookie
            self.cookie["sessionId"] = sessionId
            #load the new sessino data
            self.sessionData = SESSION_STORE.getSessionData(sessionId)
        self.cookie["sessionId"]["samesite"] = "None"
        self.cookie["sessionId"]["secure"] = True

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        super().end_headers()

    
    
    #GET one place
    def handleRetrievePlace(self, place_id):
        if "userId" not in self.sessionData:
            print("user is not logged in")
            self.handle401()
            return
        
        db = PlacesDB()
        # qurey the db for the place with id place_id
        place = db.getOnePlace(place_id)
 
        if place != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(place), "utf-8"))
        else:
            self.handleNotFound()
    
    #GET all places
    def handleRetrievePlaces(self):
        if "userId" not in self.sessionData:
            print("user is not logged in")
            self.handle401()
            return
            #print("user ID is:", self.sessionData["userId"])
        #else:
            #print("user not logged in")


        self.send_response(200)
        self.send_header("Content-Type","application/json")
        
        
        self.end_headers()
        
        ##this is to save to the file
        db = PlacesDB()
        places = db.getAllPlaces()
        
        self.wfile.write(bytes(json.dumps(places), "utf-8"))
    

    #POST 
    def handleCreateUser(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)
        
        
        user_name = parsed_body['name'][0]
        user_last = parsed_body['last'][0]
        user_email = parsed_body['email'][0]
        user_password = parsed_body['password'][0]
        
        
        
        db = UsersDB()
        email = db.validateEmail(user_email)
        #if non-existent
        if email == None:
            db.createUser(user_name, user_last, user_email, user_password)
            self.send_response(201)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Created", "utf-8"))
            print("success!")
        else:
            self.handleError()
            print("already exists!")

            


    def handleAuthenticateUser(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)
        
        user_email = parsed_body['email'][0]
        user_password = parsed_body['password'][0]
                     
        db = UsersDB()
        email = db.validateEmail(user_email)
        if email != None:
            password = db.validatePassword(user_password, user_email)
            if password == True:                   
                self.send_response(201)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("Created", "utf-8"))
                user = db.getUser(user_email)
                self.sessionData["userId"] = user["id"] ## user["id"] ##added in class
                print("Success  authentication")
            else:
                self.handleError()
                print("Wrong password")
        else:
            self.handleNotFound()
            print("Email not in DB")

    def handleCreatePlace(self):
        if "userId" not in self.sessionData:
            print("user is not logged in")
            self.handle401()
            return

        #1. read the incoming request body
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)
        
        #2. parse the request body (urlencoded data)
        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)
        
        #3. retrieve vacation data from the parsed body
        
        place_city = parsed_body['city'][0]
        place_state = parsed_body['state'][0]
        place_country = parsed_body['country'][0]
        place_activity = parsed_body['activity'][0]
        place_language = parsed_body['language'][0]
        place_climate = parsed_body['climate'][0]
        #4. append the vacation place to the array above
        #PLACES.append(place_name)
        
        ##this is to save to the file
        db = PlacesDB()
        db.createPlace(place_city,place_state, place_country, place_activity, place_language, place_climate )

        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Created", "utf-8"))
    
    
   
    def handleUpdatePlace(self, member_id):
        if "userId" not in self.sessionData:
            print("user is not logged in")
            self.handle401()
            return

        db = PlacesDB()
        
        place = db.getOnePlace(member_id)
 
        if place != None:
            length = int(self.headers["Content-Length"])
            request_body = self.rfile.read(length).decode("utf-8")
            print("raw request body: ", request_body)
            
            
            parsed_body = parse_qs(request_body)
            print("Parsed body: ", parsed_body)
            
            place_city = parsed_body['city'][0]
            place_state = parsed_body['state'][0]
            place_country = parsed_body['country'][0]
            place_activity = parsed_body['activity'][0]
            place_language = parsed_body['language'][0]
            place_climate = parsed_body['climate'][0]
            

            db.updatePlace(member_id, place_city,place_state, place_country, place_activity, place_language, place_climate )

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Updated", "utf-8"))
        else:
            self.handleNotFound()


    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))
    
    def handleError(self):
        self.send_response(422)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Already exists.", "utf-8"))
    
    def handle401(self):
        self.send_response(401)
        self.end_headers()

    def handleDeletePlace(self, place_id):
        if "userId" not in self.sessionData:
            print("user is not logged in")
            self.handle401()
            return

        db = PlacesDB()
        # query the db for the place with id place_id
        place = db.getOnePlace(place_id)
 
        if place != None:
            db.deletePlace(place_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(place), "utf-8"))
        else:
            self.handleNotFound()
        

    def do_POST(self):
        self.load_session()
        print("the post path is: ", self.path)
  
        if self.path== "/places":
            self.handleCreatePlace()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleAuthenticateUser()
        else:
            self.handleNotFound()
 
    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers() #Access-Control-Allow-Origin sent by end_headers()
    
  
    def do_PUT(self):
        self.load_session()
        print("the request path is: ", self.path)
        parts = self.path.split("/")

        collection = parts[1]
        if len(parts) > 2 :
            member_id = parts[2]
        else:
            member_id = None

        if collection == "places":
            if member_id:
                self.handleUpdatePlace(member_id)
            else:
                self.handleNotFound()

    def do_DELETE(self):
        self.load_session()
        print("the request path is: ", self.path)
        parts = self.path.split("/")

        collection = parts[1]
        if len(parts) > 2 :
            member_id = parts[2]
        else:
            member_id = None

        if collection == "places":
            if member_id:
                self.handleDeletePlace(member_id)
            else:
                self.handleNotFound()

    def do_GET(self):
        self.load_session()
        # ingredients for an HTTP reponse?
        # status code (require), headers (optional), body (optional)
        print("the request path is: ", self.path)
        parts = self.path.split("/")

        collection = parts[1]
        if len(parts) > 2 :
            member_id = parts[2]
        else:
            member_id = None

        if collection == "places":
            if member_id:
                self.handleRetrievePlace(member_id)
            else:
                self.handleRetrievePlaces()
        else:
            self.handleNotFound()
        
        '''
        if self.path== "/places":
            self.handleRetrievePlaces()

        else:
            self.handleNotFound()
        '''

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run():
    db = PlacesDB()
    db.createPlacesTable()
    db = None #disconnect from DB

    db = UsersDB()
    db.createUsersTable()
    db = None #disconnects

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = ThreadedHTTPServer(listen,MyRequestHandler)
    
    #start the server
    print("The server is running!")
    server.serve_forever()

run()
