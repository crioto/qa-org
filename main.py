#!/usr/local/bin/python3
# Subutai Test Automation Organization

import sys
import configuration as c
import repository as r

def main():
  if len(sys.argv) < 2:
    print("Path to configuration file wasn't specified. Exiting")
    exit(1)

  config = c.Configuration(sys.argv[1])
  
  repo = r.Repository(config)
  repo.extractRepositoryName()

if __name__ == '__main__': 
  main() 