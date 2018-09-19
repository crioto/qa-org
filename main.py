#!/usr/local/bin/python3
# Subutai Test Automation Organization

import sys
import os
import configuration as c
import repository as r
import utils as u
import builder as b
import analyzer as a

def main():
  if len(sys.argv) < 2:
    print("Path to configuration file wasn't specified. Exiting")
    exit(1)

  config = c.Configuration(sys.argv[1])
  
  repo = r.Repository(config.getRepo(), config)
  if repo.checkIfExists() == True:
    print("Updating repository " + repo.extractRepositoryName())
    repo.Pull()
  else:
    print("Cloning repository: " + repo.extractRepositoryName())
    repo.Clone()

  qaRepo = r.Repository(config.getQA(), config)
  if config.getRepo() != config.getQA():
    if qaRepo.checkIfExists() == True:
      print("Updating repository " + qaRepo.extractRepositoryName())
      qaRepo.Pull()
    else:
      print("Cloning repository: " + qaRepo.extractRepositoryName())
      qaRepo.Clone()
  else:
    print("Skipping QA repository: it's the same as test repo")

  if not u.CheckRepoPathExists(config, repo, config.getPath()):
    print("Configured directory " + config.getPath() + " wasn't found in test repository. Aborting")
    exit(21)

  if not u.CheckRepoPathExists(config, qaRepo, config.getQAPath()):
    print("Configured directory " + config.getQAPath() + " wasn't found in test repository. Aborting")
    exit(22)

  builder = b.Builder(config.getLocalPath() + '/' + qaRepo.extractRepositoryName() + '/' + config.getQAPath())
  builder.Run()

  analyzer = a.Analyzer(config.getLocalPath() + '/' + repo.extractRepositoryName() + '/' + config.getPath(), [])
  analyzer.Run()

if __name__ == '__main__': 
  main() 