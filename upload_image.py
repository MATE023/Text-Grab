from github import Github
g = Github("*******************************")

repo = g.get_user().get_repo("image")
files = []

def upload_image(imagename):
    #fileLoc = '/' + imagename
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            files.append(str(file).replace('ContentFile(path="','').replace('")', ''))
            
    with open(imagename, 'rb') as file:
        content = file.read()
        
    git_prefix = 'imagefolder/'
    git_file = git_prefix + imagename
    
    if git_file in files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="main")
        print(git_file + ' CREATED')
