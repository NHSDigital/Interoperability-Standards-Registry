# checkout_repos.py

import json
import subprocess

# Load repositories from master_variables.json
with open("master_variables.json") as f:
    repos = json.load(f)['repos']

# Clone each repository
for repo in repos:
    subprocess.run(["git", "clone", repos], check=True)
