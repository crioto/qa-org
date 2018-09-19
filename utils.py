# Utility functions

import os 


def CheckRepoPathExists(config, repo, dirname):
    if not os.path.exists(config.getLocalPath() + '/' + repo.extractRepositoryName() + '/' + dirname):
        return False
    
    return True


# BuildHandles will split path in two parts - full XXX-YYY-ZZZ form and relative ZZZ
def BuildHandles(path, strip):
    if path[0:len(strip)] == strip:
        np = path[len(strip):]
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

        if relative == '':
            raise ValueError("Failed to build relative path")
        
        if absolute == '':
            raise ValueError("Failed to build absolute path")

        return (absolute, relative)

    return ()