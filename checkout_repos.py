import json
import subprocess

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

# Debugging: Print each repository URL to check for errors
for repo in repos:
    print(f"Cloning repository: {repo}")
    subprocess.run(["git", "clone", repos], check=True)
