from time import sleep
import requests
import subprocess
import json

REPO_URL = "https://api.github.com/repos/LlamaCodeStudios/updates-test"
BRANCH = "main"

def get_latest_version():
    url = f"{REPO_URL}/tags"
    try:
        response = requests.get(url)
        response.raise_for_status()
        tags = response.json()
        return tags[0]["name"] if tags else None
    except Exception as e:
        print(f"Error fetching version: {e}")
        return None

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
    subprocess.run(["git", "pull"], check=True)

def main():
    latest = get_latest_version()
    local = load_local_version()

    if latest and latest != local:
        print(f"🔄 New version available: {latest} (current: {local})")
        choice = input("Do you want to update now? (y/n): ").strip().lower()
        if choice == 'y':
            update_repo()
            save_local_version(latest)
            print("✅ Update complete.")
        else:
            print("⚠️ Skipping update. You may be running an outdated version.")
    else:
        print("✅ You're running the latest version.")

if __name__ == "__main__":
    main()

sleep(3.0)