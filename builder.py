# Builder is used to build an issues tructure from a QA repository

import os
import utils as u
from itertools import chain

class IssueFile:

    fullPath = ''
    name = ''
    strip = ''
    relativeHandle = ''
    absoluteHandle = ''

    def __init__(self, path, strip):
        self.fullPath = path
        self.name = os.path.basename(path)
        self.strip = strip


    def GetType(self):
        return 'issue'


    def BuildHandles(self):
        try:
            handles = u.BuildHandles(self.fullPath, self.strip)
            if len(handles) != 2:
                raise ValueError("Result isn't full " + str(handles))
            
            self.absoluteHandle = handles[0]
            self.relativeHandle = handles[1]
        except ValueError as err:
            print("Failed to build handles: " + str(err))   

    
    def GetRelativeHandle(self):
        return self.relativeHandle


    def GetAbsoluteHandle(self):
        return self.absoluteHandle


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
    strip = ''
    name = ''
    subcats = []
    issues = []
    # From path in form of XXX-YYY-ZZZ this will take ZZZ 
    relativeHandle = '' 
    # From path in form of XXX-YYY-ZZZ this will be XXX-YYY-ZZZ 
    absoluteHandle = ''

    def __init__(self, path, strip):
        self.fullPath = path
        self.strip = strip
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


    def GetSubCategories(self):
        return self.subcats


    def GetIssues(self):
        return self.issues


    def GetAbsoluteHandle(self):
        return self.absoluteHandle


    def GetRelativeHandle(self):
        return self.relativeHandle


    def BuildHandles(self):
        try:
            handles = u.BuildHandles(self.fullPath, self.strip)
            if len(handles) != 2:
                raise ValueError("Result isn't full")
            
            self.absoluteHandle = handles[0]
            self.relativeHandle = handles[1]
        except ValueError as err:
            print("Failed to build handles: " + str(err))   


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

    
    # Scan will analyze contents of the current directory
    # This method will recursively call Scan() on every sub-object (directory)
    def Scan(self):
        d = os.listdir(self.fullPath)
        print("Scanning " + self.fullPath)
        for f in d:
            fp = os.path.join(self.fullPath, f)
            if os.path.isdir(fp):
                newDir = IssueCategory(fp, self.strip)
                newDir.Scan()
                newDir.BuildHandles()
                self.Append(newDir)
            elif os.path.isfile(fp):
                newIssue = IssueFile(fp, self.strip)
                newIssue.BuildHandles()
                self.Append(newIssue)
        return 0


    # Some woodoo magic is happening here. TODO: Fix it
    def Iterate(self):
        list = []
        #for s in self.subcats:
            #print(s.GetAbsoluteHandle())
            #list.extend(s.Iterate())

        for i in self.issues:
            list.append(i)

        return list


# Builder will build a tree of categories and issues from provided path
class Builder:

    path = ''
    tree = []

    def __init__(self, path):
        self.path = path


    def Run(self):
        print("Building issues layout from " + self.path)
        top = IssueCategory(self.path, self.path)
        top.Scan()
        self.tree = top.Iterate()
        for i in self.tree:
            print(i.GetAbsoluteHandle())
        return True

    def Get(self):
        return self.tree