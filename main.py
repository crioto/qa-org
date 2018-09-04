#!/usr/bin/python3
# Subutai Test Automation Organization

import sys
import configuration as c

def main():
  if len(sys.argv) < 2:
    print("Path to configuration file wasn't specified. Exiting")
    exit(1)

  config = c.Configuration(sys.argv[1])
  



if __name__ == '__main__': 
  main()