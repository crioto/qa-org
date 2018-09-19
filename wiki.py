# This file generates wiki pages from test coverage information

class Wiki:

  url = ''

  def __init__(self, wikiURL):
    self.url = wikiURL

  # Build method will create a table of data based on all tests, putting information about covered tests
  def Build(self, all, covered):
    
    return 0