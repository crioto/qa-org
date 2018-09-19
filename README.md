# qa-org
This is an attempt to automate automatization of testing

Original idea was proposed in optdyn/qa#61

Requires `pyyaml`, `PyGithub`

Installed `git` CLI tool must be configured with write access to the configured repository

### Installation and Configuration

It is recommended to create a separate user in a system to run this tool. Also, a separate github user

1. Configure your git application and setup your SSH key


### Implementation plan

1. Implement configuration ✓
2. Implement repository read: clone/pull ✓
3. Implement recursive reader for files in repository ✓
4. Implement reader of issues from repository files ✓
5. Implement code analyzer to find test tags ✓
6. Implement issue puller 
7. Implement wiki page generator
8. Implement repository push for wiki
9. Implement automatic issue creation
10. Implement issue updater
11. Implement GitHub webhook for repository update events