# GitHub-related functions

#from github import Github

import os
import cryptography 
import jwt
import datetime
from pytz import timezone
import json
import requests

def InitializeGithub(token):
  #g = Github(token)
  #return g
  return 0


class AppOwner:

  def __init__(self, data):
    self.login = data['login']
    self.id = data['id']
    self.node_id = data['node_id']


class AppData:

  def __init__(self, data):
    if 'id' not in data:
      return
    self.id = data['id']
    self.NodeID = data['node_id']
    self.owner = AppOwner(data['owner'])
    self.name = data['name']
    self.description = data['description']
    self.externalURL = data['external_url']
    self.htmlURL = data['html_url']
    self.created = data['created_at']
    self.updated = data['updated']


class GitHub:

  def __init__(self, pk, appID):
    self.pk = pk
    self.appID = appID
    self.jwtTime = datetime.datetime(1970,1,1)
    self.jwt = ''
    self.pkContent = ''
    self.installationID = 342761
    self.appData = AppData({})
    try:
      if self.readPK() != True:
        print("Failed to read Private Key: " + pk)
        raise ValueError("PK Read Failed")
    except ValueError as err:
      raise err


  def Auth(self):
    self.checkJWT()
    if len(self.jwt) == 0:
      return
    
    # curl -i -H "Authorization: Bearer YOUR_JWT" -H "Accept: application/vnd.github.machine-man-preview+json" https://api.github.com/app
    headers = {
      "Accept": "application/vnd.github.machine-man-preview+json",
      "Authorization": "Bearer " + str(self.jwt)
    }
    r = requests.get("https://api.github.com/app", headers=headers)
    self.processAppData(json.dumps(r.content.decode('utf-8')))
    

  def processAppData(self, data):
    self.appData = AppData(data)
    print("App info: " + self.appData.name)


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
    tz = timezone("Asia/Bishkek")
    ct = datetime.datetime.now(tz)
    ctf = ct + datetime.timedelta(0, 60*9)
    data = {
      #'iat': int((ct  - datetime.datetime(1970,1,1)).total_seconds()),
      #'exp': int((ctf  - datetime.datetime(1970,1,1)).total_seconds()),
      'iat': int(ct.timestamp()),
      'exp': int(ctf.timestamp()),
      'iss': self.appID
    }
    print(data)
    
    js = json.dumps(data)
    self.jwt = jwt.encode(data, self.pkContent, 'RS256').decode('utf-8')
    self.jwtTime = ct
    return 0
  

  def checkJWT(self):
    delta = datetime.datetime.now() - self.jwtTime
    if delta.total_seconds() >= (60*90):
      print("JWT expired")
      self.createJWT()