# checkout_repos.py

import json
import subprocess

# Load repositories from master_variables.json
with open("master_variables.json") as f:
    repos = json.load(f)['repos']
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

# Clone or pull each repository
for repo in repos:
    repo_name = repo.split('/')[-1]  # Extract the repo name from the URL
    if os.path.isdir(repo_name):
        # If the directory exists, pull the latest changes
        print(f"Directory {repo_name} exists, pulling latest changes.")
        subprocess.run(["git", "-C", repo_name, "pull"], check=True)
    else:
        # Otherwise, clone the repository
        print(f"Cloning repository: {repo}")
        subprocess.run(["git", "clone", repo], check=True)


# Clone each repository
for repo in repos:
    subprocess.run(["git", "clone", repos], check=True)
    
