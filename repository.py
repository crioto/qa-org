# This file is for git tool to download/update repository with tests
# `git` application must be installed and available in PATH or specified in configuration file
# `local_path` can be specified in configuration. If not specified, /tmp will be used

import configuration as c
from urllib.parse import urlparse

class Repository:

  repoName = ''

  def __init__(self, config):
    self.config = config
    self.repoName = self.extractRepositoryName()
    

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
    return 0