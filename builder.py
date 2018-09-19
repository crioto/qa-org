# Builder is used to build an issues tructure from a QA repository

import os

class IssueFile:

    fullPath = ''
    name = ''
    strip = ''


    def __init__(self, path, strip):
        self.path = path
        self.name = os.path.basename(path)
        self.strip = strip

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


    # BuildHandles will split path in two parts - full XXX-YYY-ZZZ form and relative ZZZ
    def BuildHandles(self):
        if self.fullPath[0:len(self.strip)] == self.strip:
            np = self.fullPath[len(self.strip):]
            if np[:1] == '/':
                np = np[1:]

            parts = np.split('/')
            absolute = ''
            relative = ''
            i = 0
            for p in parts:
                absolute += p
                i += 1
                if len(parts) == i:
                    relative = p
                else:
                    absolute += '-'

            print("Relative: " + relative + " Absolute: " + absolute)
        return 0

    
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
                self.Append(newIssue)
        return 0


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
        # self.ProcessDirectory()
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