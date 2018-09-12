# configuration.py reads configuration and stores it in the object

# Configuration is provided to the application in the YAML format
# stored in a file. The following configuration options are available:
# `gh_token` - Token to access GitHub API
# `repo` - Repository of test code in a way it can be red by CLI git client (usually starts with git:// or https://)
# `qa_repo` - Repository of issues
# `path` - Path to QA database inside the repository

import yaml 
import os

class Configuration:

    token = ''
    repo = ''
    qa = ''
    path = ''
    git = ''
    localPath = '/tmp'
    configPath = ''

    def __init__(self, configPath):
        self.configPath = configPath
        with open(configPath, 'r') as stream:
            try:
                c = yaml.load(stream)
                self.token = c['gh_token']
                self.repo = c['repo']
                self.path = c['path']
                self.qa = c['qa_repo']
                if 'git' in c:
                    self.git = c['git']
                else:
                    self.git = 'git'
                if 'local_path' in c:
                    self.localPath = c['local_path']
            except yaml.YAMLError as exc:
                print(exc)
                exit(5)

        if self.token == '':
            print("Missing GitHub token. Exiting")
            exit(2)
        
        if self.repo == '':
            print("Repository wasn't specified. Exiting")
            exit(3)

        if self.path == '':
            print("Path to tests code not specified. Exiting")
            exit(4)

        if len(self.git) > 3 and self.checkGit(self.git) != True:
            print("git binary specified in options was not found or it's not executable")
            exit(6)
        elif self.findGitInPath() != True:
            print("git binary wasn't found in PATH")
            exit(7)

        if self.qa == '':
            print("QA Repository wasn't specified. Exiting")
            exit(8)

        


    def getToken(self):
        return self.token


    def getRepo(self):
        return self.repo


    def getQA(self):
        return self.qa

    
    def getPath(self):
        return self.path


    def getLocalPath(self):
        return self.localPath


    def checkGit(self, gitPath):
        return os.path.isfile(gitPath) and os.access(gitPath, os.X_OK)


    def findGitInPath(self):
        for path in os.environ["PATH"].split(os.pathsep):
            git = path + "/git"
            if self.checkGit(git) == True:
                return True

        return False