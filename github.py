# GitHub-related functions

#from github import Github

import os
import cryptography 
import jwt
import datetime
import json

def InitializeGithub(token):
  #g = Github(token)
  #return g
  return 0

class GitHub:

  pk = ''
  appID = ''
  pkContent = ''
  jwt = ''
  jwtTime = datetime.datetime

  def __init__(self, pk, appID):
    self.pk = pk
    self.appID = appID
    try:
      if self.readPK() != True:
        print("Failed to read Private Key: " + pk)
        raise ValueError("PK Read Failed")
    except ValueError as err:
      raise err


  def Auth(self):
    self.checkJWT()


  def readPK(self):
    if not os.path.exists(self.pk):
      raise ValueError("Private Key file doesn't exists")
    f = open(self.pk, "r")
    self.pkContent = f.read()
    if len(self.pkContent) > 0:
      return True
    return False

  def createJWT(self):
    print("Creating new JWT")
    ct = datetime.datetime.now()
    ctf = ct + datetime.timedelta(0, 60*9)
    data = {
      'iat': (ct  - datetime.datetime(1970,1,1)).total_seconds(),
      'exp': (ctf  - datetime.datetime(1970,1,1)).total_seconds(),
      'iss': self.appID
    }
    js = json.dumps(data)
    print(js)
    self.jwt = jwt.encode(js, self.pkContent, 'RS256')
    self.jwt = ct
    return 0
  

  def checkJWT(self):
    delta = self.jwtTime - datetime.datetime.now()
    if delta >= (60*90):
      print("JWT expired")
      self.createJWT()