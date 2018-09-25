# GitHub-related functions

#from github import Github

import os
import cryptography 
import jwt
import datetime
#from pytz import timezone
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
    if 'node_id' in data:
      self.NodeID = data['node_id']
    if 'owner' in data:
      self.owner = AppOwner(data['owner'])
    if 'name' in data:
      self.name = data['name']
    if 'description' in data:
      self.description = data['description']
    if 'external_url' in data:
      self.externalURL = data['external_url']
    if 'html_url' in data:
      self.htmlURL = data['html_url']
    if 'created_at' in data:
      self.created = data['created_at']
    if 'updated_at' in data:
      self.updated = data['updated_at']


class GitHub:

  url = 'https://api.github.com'

  def __init__(self, pk, appID):
    self.pk = pk
    self.appID = appID
    self.jwtTime = datetime.datetime(1970,1,1,0,0,0,0, datetime.timezone.utc)
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


  def buildEP(self, suffix):
    return self.url + suffix


  def Auth(self):
    self.checkJWT()
    if len(self.jwt) == 0:
      return
    
    headers = {
      "Accept": "application/vnd.github.machine-man-preview+json",
      "Authorization": "Bearer " + str(self.jwt)
    }
    r = requests.get(self.buildEP('/app'), headers=headers)
    
    self.processAppData(json.loads(r.content.decode('utf-8')))


  # CheckUserInstallation will request installation for specified user
  def CheckUserInstallation(self, handle):
    return self.checkInstallation('users', handle)


  def CheckOrgInstallation(self, handle):
    return self.checkInstallation('orgs', handle)


  def checkInstallation(self, instType, handle):
    if instType != 'orgs' and instType != 'users':
      print("No suitable type specified. User assumed")
      instType = 'users'

    headers = {
      "Accept": "application/vnd.github.machine-man-preview+json",
      "Authorization": "Bearer " + str(self.jwt)
    }

    r = requests.get(self.buildEP('/'+instType+'/'+handle+'/installation'), headers=headers)
    data = json.loads(r.content.decode('utf-8'))
    if 'target_id' in data:
      return data['target_id']
    return -1


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
    ct = datetime.datetime.now(datetime.timezone.utc)
    ctf = ct + datetime.timedelta(0, 60*9)
    data = {
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
    delta = datetime.datetime.now(datetime.timezone.utc) - self.jwtTime
    if delta.total_seconds() >= (60*90):
      print("JWT expired")
      self.createJWT()