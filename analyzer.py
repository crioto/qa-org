# Analyzer walks through the code files (*.py) and searches for
# configured tags

import os


class Match:

  tag = ''
  source = ''
  line = -1

  def __init__(self, tag, source, line):
    self.tag = tag
    self.source = source
    self.line = line


  def GetTag(self):
    return self.tag


  def GetSource(self):
    return self.source


  def GetLine(self):
    return self.line


class Analyzer:

  path = ''
  tags = []
  matches = []

  def __init__(self, path, tags):
    self.path = path
    self.tags = tags


  # Run will go through the list of directories and find all source code files
  # open each file and search for test tags.
  def Run(self):
    print("Starting analyzer for " + self.path)
    for root, subdirs, files in os.walk(self.path):
      for f in files:
        if f.endswith('.py'):
          self.File(os.path.join(root, f))

    return 0


  def File(self, filepath):
    f = open(filepath, "r")
    buffer = f.read()
    lines = buffer.split("\n")
    lc = 0
    for line in lines:
      for tag in self.tags:
        subject = "# " + tag
        if line.strip()[:len(subject)] == subject:
          self.matches.append(Match(tag, filepath, lc))

      lc += 1


  def GetMatches(self):
    return self.matches