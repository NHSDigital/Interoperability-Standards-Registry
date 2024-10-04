import json
import subprocess
import os  # Make sure os is imported

# Load repositories from master_variables.json
try:
    with open("main_variables.json") as f:
        data = json.load(f)
        repos = data.get('repos', None)
        if repos is None:
            raise KeyError('repo_list not found in master_variables.json')
except FileNotFoundError:
    print("master_variables.json file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error parsing master_variables.json. Make sure it is valid JSON.")
    exit(1)
except KeyError as e:
    print(f"KeyError: {e}")
    exit(1)

# Function to clone or pull the repository
def clone_or_pull_repo(repo_url):
    repo_name = repo_url.split('/')[-1].replace('.git', '')  # Extract the repo name
    repo_dir = os.path.join('repos', repo_name)  # Define the directory where the repo will be cloned

    if os.path.isdir(repo_dir):
        # If the directory exists, pull the latest changes
        print(f"Directory {repo_dir} exists, pulling latest changes.")
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
    else:
        # Otherwise, clone the repository
        print(f"Cloning repository: {repo_url}")
        os.makedirs(repo_dir, exist_ok=True)
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)

# Iterate through the list of repositories and clone or pull
for repo in repos:
    try:
        clone_or_pull_repo(repo)
    except subprocess.CalledProcessError as e:
        print(f"Error while processing {repo}: {e}")

