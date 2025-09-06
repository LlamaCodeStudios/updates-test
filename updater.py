import requests
import subprocess
import json

REPO_URL = "https://api.github.com/repos/yourusername/snake_game"
BRANCH = "main"

def get_latest_commit():
    url = f"{REPO_URL}/commits/{BRANCH}"
    response = requests.get(url)
    return response.json()["sha"]

def load_local_version():
    try:
        with open("config.json") as f:
            return json.load(f)["version"]
    except:
        return None

def save_local_version(version):
    with open("config.json", "w") as f:
        json.dump({"version": version}, f)

def update_repo():
    subprocess.run(["git", "pull"])

def main():
    latest = get_latest_commit()
    local = load_local_version()
    if latest != local:
        print("🔄 Updating game...")
        update_repo()
        save_local_version(latest)
    else:
        print("✅ Game is up to date.")

if __name__ == "__main__":
    main()
