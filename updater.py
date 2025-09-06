import requests
import subprocess
import json

REPO_URL = "https://api.github.com/repos/LlamaCodeStudios/updates-test"
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

    if not latest:
        print("⚠️ Unable to check for updates. Proceeding with local version.")
        return

    if latest != local:
        print("\n" + "="*50)
        print("🚨 WARNING: Your version is outdated!")
        print(f"🔄 Latest version: {latest}")
        print(f"📦 Local version: {local}")
        print("💡 It's recommended to update before launching.")
        print("="*50 + "\n")

        choice = input("Do you want to update now? (y/n): ").strip().lower()
        if choice == 'y':
            update_repo()
            save_local_version(latest)
            print("✅ Update complete.")
        else:
            print("⚠️ Skipping update. You may encounter issues.")
    else:
        print("✅ Game is up to date.")


if __name__ == "__main__":
    main()
