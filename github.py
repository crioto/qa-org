# GitHub-related functions

from github import Github

def InitializeGithub(token):
  g = Github(token)
  return g