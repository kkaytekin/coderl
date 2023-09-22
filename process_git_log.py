import os
import subprocess

def get_hashes_from_txt(file_path, debug='vvv'):
    with open(file_path,'r') as f:
        log_list = f.read().splitlines()

    hashes = []
    for line in log_list:
        hashes.append(line.split(' ')[0])
    if debug == 'vvv':
        print(hashes)
    return hashes

def get_commits(path,debug = 'vvv'):
    '''
    path: path_to_repo_dir
    out: list of commits, ordered from oldest to newest. Each commit is a dict with keys{commit_hash, commit_message, commit_body}
    '''
    # Save the current work_dir, because we are gonna return there in the end.
    cwd = os.getcwd()
    assert os.path.isdir(path)
    os.chdir(path)
    print(f"Cwd: {os.getcwd()}")
    # Run the command and capture its output
    delimiter = "QXTZbhjIdReBbD"
    hash_msg_splitter = "dTgNlDxcfwAgscWrdxyD"
    msg_body_splitter = "srWqavXdfwFaxVdFwaSF"
    commits = subprocess.getoutput(f'git log --format="%H{hash_msg_splitter}%s{msg_body_splitter}%b{delimiter}"')
    commits = commits.split(delimiter)
    # The last element is an empty string
    assert commits[-1] == ''
    commits = commits[:-1] 
    out = []
    for cmt in commits:
        info = {}
        # Get commit hash and message
        cmt_hash, cmt_msg_and_body = cmt.split(hash_msg_splitter)
        # From the second entry onwards, hashes start with newline. We dont want that
        cmt_hash = cmt_hash.replace('\n','')
        assert len(cmt_hash) == 40
        info['commit_hash'] = cmt_hash

        # Get the commit body. If no body, save empty string
        if cmt_msg_and_body[-len(msg_body_splitter):] == msg_body_splitter:
            cmt_msg = cmt_msg_and_body[:-len(msg_body_splitter)]
            cmt_body = ''
        else:
            cmt_msg, cmt_body = cmt_msg_and_body.split(msg_body_splitter)
        info["commit_message"] = cmt_msg
        info['commit_body'] = cmt_body
        out.append(info)
    assert len(out) == len(commits)

    os.chdir(cwd)
    print(f"Cwd: {os.getcwd()}")
    # Now the commits are listed from newest to oldest.
    # We inverse the ordering
    return out[::-1]

def get_tag_hashes(path):
    '''
    # TODO
    Get the commit hashes of tags for a more advanced dataset.
    This dataset consists of harder examples because diffs are between distinct commits.
    Each tag is a new version of the library. 
    '''
    pass

def get_hash_pairs(commits):
    '''
    Get pairs of hashes, from oldest the newest.
    '''
    hash_pairs = []
    for i in range(len(commits)-1):
        old = commits[i]["commit_hash"]
        new = commits[i+1]["commit_hash"]
        hash_pairs.append((old,new))
    return hash_pairs

if __name__ == '__main__':
    commits = get_commits('/home/kagan/coderl/gym-md')
    diffs_list = get_hash_pairs(commits)