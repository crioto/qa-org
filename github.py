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
    self.installationID = 0
    self.appData = AppData({})
    self.token = ''
    self.tokenExp = datetime.datetime(1970,1,1,0,0,0,0, datetime.timezone.utc)
    try:
      if self.readPK() != True:
        print("Failed to read Private Key: " + pk)
        raise ValueError("PK Read Failed")
    except ValueError as err:
      raise err


  def buildEP(self, suffix):
    print(self.url + suffix)
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


  def AuthInstallation(self, id):
    self.installationID = id
    self.checkJWT()
    if len(self.jwt) == 0:
      raise ValueError("Broken JWT")

    headers = {
      "Accept": "application/vnd.github.machine-man-preview+json",
      "Authorization": "Bearer " + str(self.jwt)
    }
    r = requests.post(self.buildEP('/app/installations/'+str(self.installationID) + '/access_tokens'), headers=headers)
    if r.headers['Status'] != '201 Created':
      raise ValueError('Failed to authenticate installation')
      
    tokenData = json.loads(r.content.decode('utf-8'))
    self.token = tokenData['token']
    self.tokenExp = datetime.datetime.strptime(tokenData['expires_at'], '%Y-%m-%dT%H:%M:%SZ')




  # CheckUserInstallation will request installation for specified user
  def CheckUserInstallation(self, handle):
    return self.checkInstallation('users', handle)


  def CheckOrgInstallation(self, handle):
    return self.checkInstallation('orgs', handle)


  def CheckRepoInstallation(self, uhandle, rhandle):
    return self.checkInstallation("repos/"+uhandle, rhandle)


  def checkInstallation(self, instType, handle):
    if instType != 'orgs' and instType != 'users' and instType[0:5] != 'repos':
      print("No suitable type specified. User assumed")
      instType = 'users'

    headers = {
      "Accept": "application/vnd.github.machine-man-preview+json",
      "Authorization": "Bearer " + str(self.jwt)
    }

    r = requests.get(self.buildEP('/'+instType+'/'+handle+'/installation'), headers=headers)
    data = json.loads(r.content.decode('utf-8'))
    if 'target_id' in data:
      if instType[0:5] == 'repos':
        return data['id']
      else:
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
    
    js = json.dumps(data)
    self.jwt = jwt.encode(data, self.pkContent, 'RS256').decode('utf-8')
    self.jwtTime = ct
    return 0
  

  def checkJWT(self):
    delta = datetime.datetime.now(datetime.timezone.utc) - self.jwtTime
    if delta.total_seconds() >= (60*90) or self.jwt == '':
      print("JWT expired")
      self.createJWT()


  def GetIssues(self, user, repo):
    headers = {
      "Accept": "application/vnd.github.symmetra-preview+json",
      "Authorization": "token " + self.token
    }

    r = requests.get(self.buildEP('/repos/'+user+'/'+repo+'/issues'), headers=headers)
    data = json.loads(r.content.decode('utf-8'))

    print(data)

  
  def CreateIssue(self, user, repo, title, text, labels):
    headers = {
      "Accept": "application/vnd.github.symmetra-preview+json",
      "Authorization": "token " + self.token
    }

    data = {
      "title": title,
      "body": text
    }

    r = requests.post(self.buildEP('/repos/'+user+'/'+repo+'/issues'), data=json.dumps(data), json="", headers=headers)
    print(r.content)
