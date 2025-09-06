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
        if tags:
            return tags[0]["name"]  # Assumes latest tag is first
        else:
            return None
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch tags: {e}")
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
    subprocess.run(["git", "pull"])

def main():
    latest = get_latest_version()
    local = load_local_version()

    if not latest:
        print("⚠️ Could not retrieve latest version.")
        return

    if latest != local:
        print(f"\n🚨 New version available: {latest} (current: {local})")
        choice = input("Update now? (y/n): ").strip().lower()
        if choice == 'y':
            update_repo()
            save_local_version(latest)
            print("✅ Updated successfully.")
        else:
            print("⚠️ Running outdated version.")
    else:
        print("✅ You're running the latest version.")



if __name__ == "__main__":
    main()

sleep(5.0)