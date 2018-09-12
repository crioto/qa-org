# Builder is used to build an issues tructure from a QA repository

import os

class IssueFile:

    fullPath = ''
    name = ''


    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)


    def GetType(self):
        return 'issue'


    # Returns name of the issue file extracted from full path
    def GetName(self):
        if self.name != '':
            return self.name

        if os.path.exists(self.fullPath) and os.path.isfile(self.fullPath):
            self.name = os.path.basename(self.fullPath)
            return self.name
        else:
            raise ValueError(self.fullPath + "doesn't exists or it's not a file")


# IssueCategory class contains a tree-like structure of issues
# Each object may contain sub-objects of the same type or IssueFile objects
class IssueCategory:

    fullPath = ''
    name = ''
    subcats = []
    issues = []

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)


    def GetType(self):
        return 'category'


    # Returns name of the issue file extracted from full path
    def GetName(self):
        if self.name != '':
            return self.name

        if os.path.exists(self.fullPath) and os.path.isfile(self.fullPath):
            self.name = os.path.basename(self.fullPath)
            return self.name
        else:
            raise ValueError(self.fullPath + "doesn't exists or it's not a file")


    def Append(self, obj):
        try: 
            if obj.GetType() == 'category':
                self.subcats.append(obj)
            elif obj.GetType() == 'issue':
                self.issues.append(obj)
            else:
                raise ValueError("Can't append object: unknown type") 
        except Exception as err:
            e = str(err)
            print("Can't append object: bad type: " + e)


# Builder will build a tree of categories and issues from provided path
class Builder:

    path = ''
    tree = []

    def __init__(self, path):
        self.path = path


    def Run(self):
        self.ProcessDirectory()
        # print('Iterating ' + self.path)
        # for subdir, dirs, files in os.walk(self.path):
        #     for file in files:
        #         print(os.path.join(subdir, file))

        #     for directory in dirs:
        #         print(directory)

        #     print("SUB" + subdir)
    
        return True

    
    def ProcessDirectory(self):
        c = os.listdir(self.path)
        for f in c:
            if f == "README.md": 
                continue
                
            print(os.path.join(self.path, f))