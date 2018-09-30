#!/usr/local/bin/python3
# Subutai Test Automation Organization

import sys
import os
import configuration as c
import repository as r
import utils as u
import builder as b
import analyzer as a
import github as g


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

  # Workflow starts here

  gh = 0

  try:
    gh = g.GitHub(config.getPrivateKey(), config.getAppID())
    gh.Auth()
  except ValueError as err:
    print("GitHub auth failed: " + str(err))
    exit(101)

  ghUser = ''
  ghOrg = ''
  ghType = ''
  installation_id = 0

  for user in config.getUsers():
    installation_id = gh.CheckUserInstallation(user)
    ghUser = user
    ghType = 'user'
    break

  for org in config.getOrgs():
    installation_id = gh.CheckOrgInstallation(org)
    ghOrg = org
    ghType = 'org'
    break

  ghTitle = ''
  if ghType == 'user':
    ghTitle = ghUser
  else:
    ghTitle = ghOrg

  if installation_id == 0:
    print("Couldn't get installation for " + ghType + " " + ghTitle)
    exit(210)

  installation_id = gh.CheckRepoInstallation('crioto', 'qa-org')

  print("Found installation ID for " + ghTitle + ": " + str(installation_id))
  gh.AuthInstallation(installation_id)

  print(gh.GetIssues('crioto', 'qa-org'))

  gh.CreateIssue('crioto', 'qa-org', 'Test Title', 'Test Text', '')
  print(gh.GetIssues('crioto', 'qa-org'))

  # gh = g.InitializeGithub(config.getToken())
  # user = gh.get_user()
  # print(user)

  exit(0)

  builder = b.Builder(os.path.join(config.getLocalPath(), qaRepo.extractRepositoryName(), config.getQAPath()))
  builder.Run()

  issues = builder.Get()
  tags = []
  for issue in issues:
    tags.append(issue.GetAbsoluteHandle())

  analyzer = a.Analyzer(os.path.join(config.getLocalPath(), repo.extractRepositoryName(), config.getPath()), tags)
  analyzer.Run()

  covered = analyzer.GetMatches()


if __name__ == '__main__': 
  main() 