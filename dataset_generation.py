# We use the preprocessed github repository to generate a sequence of states.
# We achieve this by removing lines of code and bodies of code.
# Bodies of code are simple python indentation blocks. Including the first line of parent indentation.
# Because parent indentations include very important context information:
# for i in(range(5)):
#   print(i)
# The aim is to use these states of sequences to train an RL agent, built on CodeLlama
# S: Current state of the repository
# A: Code generated by CodeLlama
# R: End reward = Similarity to final repository.

# There is sadly high risk of overfitting. But for the first stage of the experiments
# this overfitting can be ignored, and the followup work can aim to address this overfitting.


# The first stage of the development is pulling git repositories into a folder where
# this algorithm will work on. This algorithm will work on the already pulled and extracted 
# github repository.

# I start by pulling a random repository.
# We decided to limit our focus on API repositories, because API's are functional machines.
# So the repository I chose: https://github.com/ganyariya/gym-md
# From this search of PyPI:
# https://pypi.org/search/?q=&o=&c=Topic+%3A%3A+Scientific%2FEngineering+%3A%3A+Artificial+Intelligence&c=Programming+Language+%3A%3A+Python+%3A%3A+3&c=Programming+Language+%3A%3A+Python+%3A%3A+3+%3A%3A+Only&c=Natural+Language+%3A%3A+English

import os
import zlib

def get_repos_list(path:str, debug='vvv'):
    items_list = os.listdir(path)
    repos_list = []
    for item in items_list:
        if os.path.isdir(item):
            # Ignore hidden files of the top directory (especially .git)
            if not item[0] == '.':
                repos_list.append(item)
    if debug == 'vvv':
        print(f'Repos List: {repos_list}')
    return repos_list

def get_dot_git_paths(repos_list, debug='vvv'):
    dot_git_paths = []
    for repo in repos_list:
        items = os.listdir(repo)
        if debug == 'vvv':
            print(f'Items in the repo {repo}: \n {items}')
        if '.git' in items:
            dot_git_path = os.getcwd()
            dot_git_path = os.path.join(dot_git_path,repo)
            dot_git_path = os.path.join(dot_git_path,'.git')
            dot_git_paths.append(dot_git_path)
        if debug == 'vvv':
            print(f'.git path: {dot_git_path}')
    return dot_git_paths

def explore_dot_git_contents(dot_git_path):
    for root, dirs, files in os.walk(dot_git_path):
        for file in files:
            print(os.path.join(root,file))


# Chatgpt
def extract_blob(repo_path, blob_sha):
    blob_path = os.path.join(repo_path, 'objects', blob_sha[:2], blob_sha[2:])
    with open(blob_path, 'rb') as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data

# Chatgpt
def list_blobs(repo_path):
    objects_path = os.path.join(repo_path, 'objects')
    blobs = []
    for root, dirs, files in os.walk(objects_path):
        for file in files:
            sha = os.path.join(root, file)[len(objects_path)+1:]
            blobs.append(sha)
    return blobs

if __name__ == '__main__':
    repo_path = '/path/to/.git'  # Replace with the path to your .git directory
    blobs = list_blobs(repo_path)
    
    for blob in blobs:
        data = extract_blob(repo_path, blob)
        print(f'Contents of blob {blob}:')
        print(data.decode('utf-8'))  # Assuming the content is text, change accordingly if binary


if __name__ == '__main__':
    DEBUG = 'vvv'
    cwd = os.getcwd()
    repos_list = get_repos_list(cwd,debug=DEBUG)
    dot_git_paths = get_dot_git_paths(repos_list,debug=DEBUG)
    explore_dot_git_contents(dot_git_paths[0])
