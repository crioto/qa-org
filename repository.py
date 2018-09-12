# This file is for git tool to download/update repository with tests
# `git` application must be installed and available in PATH or specified in configuration file
# `local_path` can be specified in configuration. If not specified, /tmp will be used

import os
import subprocess
import configuration as c
from urllib.parse import urlparse

class Repository:

  repoName = ''
  loc = ''

  def __init__(self, config):
    self.config = config
    self.repoName = self.extractRepositoryName()
    self.loc = config.getLocalPath()

  def extractRepositoryName(self):
    o = urlparse(self.config.getRepo())
    parts = o.path.split('/')
    repo = ''
    for p in parts:
      repo = p

    if repo[len(repo)-4:] == '.git':
      repo = repo[:len(repo)-4]

    return repo


  def checkIfExists(self):
    path = self.loc + '/' + self.extractRepositoryName()
    if os.path.exists(path):
      return True

    return False


  def Clone(self):
    path = self.loc + '/' + self.extractRepositoryName()
    p = subprocess.Popen(['git', 'clone', self.config.getRepo(), path])
    p.communicate()
    return p.returncode


  def Reset(self):
    path = self.loc + '/' + self.extractRepositoryName()
    p = subprocess.Popen(['git', 'reset', '--hard'], cwd=path)
    p.communicate()
    return p.returncode

  
  def Pull(self):
    path = self.loc + '/' + self.extractRepositoryName()
    p = subprocess.Popen(['git', 'pull'], cwd=path)
    p.communicate()
    return p.returncode