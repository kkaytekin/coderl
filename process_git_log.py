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
    out: list of commits {hash, commit msg}
    '''
    # Save the current work_dir, because we are gonna return there in the end.
    cwd = os.getcwd()
    
    assert os.path.isdir(path)
    os.chdir(path)
    print(f"Cwd: {os.getcwd()}")
    # Run the command and capture its output
    hashes = subprocess.getoutput('git log --format="%H"')
    hashes = hashes.split('\n')
    commit_msgs = subprocess.getoutput('git log --format="%s"')
    commit_msgs = commit_msgs.split('\n')
    commit_msgs_and_bodies = subprocess.getoutput('git log --format="%sğ%b"')
    commit_msgs_and_bodies = commit_msgs_and_bodies.split('ğ')
    for i in range(len(commit_msgs_and_bodies)):
        if commit_msgs_and_bodies[i][:1] == '\n':
            commit_msgs_and_bodies[i]= commit_msgs_and_bodies[i][1:]
    os.chdir(cwd)
    print(f"Cwd: {os.getcwd()}")
    commits = []
    for hash, msg in zip(hashes, commit_msgs):
        commits.append({
            'hash' : hash,
            'commit_msg' : msg
        })
    # Add the commit bodies.
    assert len(commits) == len(commit_msgs)
    for i in range(len(commit_msgs)-1):
        # Find the idx of the current commit message
        idx = commit_msgs_and_bodies.index(commit_msgs[i])
        # TODO: FIX
        # The next item in the commit_messages_and_bodes should not be the next commit message
        if commit_msgs_and_bodies[idx + 1] == commit_msgs[i+1]:
            # There is no commit body.
            commits[i]['commit_body'] = ''
        else:
            # There is commit body.
            commits[i]['commit_body'] = commit_msgs_and_bodies[idx + 1]
    # Handle the last one separately
    idx = commit_msgs_and_bodies.index(commit_msgs[-1])
    if idx == len(commit_msgs_and_bodies) - 1:
        # This is the last element. There is no commit body.
        commits[-1]['commit_body'] = ''
    else:
        # There is commit body.
        commits[-1]['commit_body'] = commit_msgs_and_bodies[-1]



    if debug == 'vvv':
        print(commits)

    return commits

def get_hash_pairs(hashes):
    '''
    Get pairs of hashes, from oldest the newest.
    '''

if __name__ == '__main__':
    get_commits('/home/kagan/coderl/gym-md')