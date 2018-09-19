# Analyzer walks through the code files (*.py) and searches for
# configured tags

import os

class Analyzer:

  path = ''
  tags = []

  def __init__(self, path, tags):
    self.path = path
    self.tags = tags


  # Run will go through the list of directories and find all source code files
  # open each file and search for test tags.
  def Run(self):
    print("Starting analyzer for " + self.path)
    for root, subdirs, files in os.walk(self.path):
      for f in files:
        print(f)
        if f.endswith('.py'):
          self.File(f)

    return 0


  def File(self, filepath):
    print("Analyzing " + filepath)