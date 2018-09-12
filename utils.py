# Utility functions

import os 


def CheckRepoPathExists(config, repo, dirname):
    if not os.path.exists(config.getLocalPath() + '/' + repo.extractRepositoryName() + '/' + dirname):
        return False
    
    return True