# Hi
# Get github repos from pypi projects queried by topic in JSON format from pipy api

from bs4 import BeautifulSoup
import requests
import threading
import queue
import subprocess
import os

def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error"
    
def get_repo_list(html):
    repoList = []
    soup = BeautifulSoup(html, "html.parser")
    for repo in soup.find_all('span', class_='package-snippet__name'):
        repoList.append(repo.string)
    return repoList

def get_projects_from_next_page(index, query):
    html = get_html('https://pypi.org/search/' + query + '&page=' + str(index))
    return get_repo_list(html)



# Get the github links from the pypi projects
def get_github_links(projects, result_queue):
    for project in projects:
        response = requests.get('https://pypi.org/pypi/' + project + '/json')
        if response.status_code == 200:
            data = response.json()

            # Get the source url
            source_url = ''
            if data and 'info' in data and data['info'] is not None and 'home_page' in data['info'] and data['info']['home_page'] is not None:
                source_url = data['info']['home_page']
            elif data and 'info' in data and data['info'] is not None and 'project_urls' in data['info'] and data['info']['project_urls'] is not None and 'Source' in data['info']['project_urls'] and data['info']['project_urls']['Source'] is not None:
                source_url = data['info']['project_urls']['Source']

            if source_url != '' and 'github.com' in source_url:
                result_queue.put(source_url)


# Get all repos from pypi using a search query
def get_all_repos(query):
    projectCount = 0
    index = 1

    threads = []
    result_queue = queue.Queue()

    print("Getting projects from PyPI...")

    while True:
        projectList = get_projects_from_next_page(index, query)
        thread = threading.Thread(target=get_github_links, args=(projectList, result_queue))
        threads.append(thread)
        thread.start()

        if len(projectList) == 0:
            break
        else:
            projectCount += len(projectList)
            index += 1

    for thread in threads:
        thread.join()

    # Collect results from the queue
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)
    
    resultCount = len(results)
    print(f"""
----------------------------------------
Fount {resultCount} github links
From {projectCount} projects on PyPI
----------------------------------------
          
          """)
    return results


def process_repo(url):
    try:
        print(f"Cloning repository {url}")
        subprocess.run(["git", "clone", url], check=True)
        repoName = url.split('/')[-1].split('.')[0]

        # Change directory to repo
        os.chdir(repoName)

        # Get commit hashes
        result = subprocess.run(['git', 'log', '--pretty=format:%h'], stdout=subprocess.PIPE, check=True)
        commit_hashes = result.stdout.decode('utf-8').split('\n')
        print(commit_hashes)

        os.chdir('..')
        
        # Change back to original directory
        subprocess.run(["cd", ".."], check=True)

        # Remove repo
        subprocess.run(["rm", "-rf", repoName], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to clone the repository.")
