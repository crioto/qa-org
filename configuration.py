# configuration.py reads configuration and stores it in the object

# Configuration is provided to the application in the YAML format
# stored in a file. The following configuration options are available:
# `gh_token` - Token to access GitHub API
# `repo` - Repository in a way it can be red by CLI git client (usually starts with git:// or https://)
# `path` - Path to QA database inside the repository

import yaml 

class Configuration:

    token = ''
    repo = ''
    path = ''
    configPath = ''

    def __init__(self, configPath):
        self.configPath = configPath
        with open(configPath, 'r') as stream:
            try:
                c = yaml.load(stream)
                self.token = c['gh_token']
                self.repo = c['repo']
                self.path = c['path']
                print(self.path)
            except yaml.YAMLError as exc:
                print(exc)

        if self.token == '':
            print("Missing GitHub token. Exiting")
            exit(2)
        
        if self.repo == '':
            print("Repository wasn't specified. Exiting")
            exit(3)

        if self.path == '':
            print("Path to tests code not specified. Exiting")
            exit(4)


    def getToken(self):
        return self.token


    def getRepo(self):
        return self.repo

    
    def getPath(self):
        return self.path