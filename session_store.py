import base64, os

class SessionStore:
    
    def __init__(self):
        #data members?
        self.sessions = {} #dictionary: keys are session IDs, values are dictionaries
   

    #generate session ID
    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    #create session (useing new session ID)
    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {} # a dictionary for THIS session
        return sessionId
    
    #get session data (by session ID)
    def getSessionData(self, sessionId):
        #ensure sessionId is valid
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
    
    #optional
    def setSessionData(self, sessionId, data):
        pass
    
   
