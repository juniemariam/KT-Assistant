# Download messages and images from Slack channels a=and have mentioned only a few chanels can add more

import os
import json
import requests
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Channels to pull from
CHANNEL_NAMES = ["general", "eng-team", "infra"]

def get_channel_id(name):
    result = client.conversations_list()
    for channel in result["channels"]:
        if channel["name"] == name:
            return channel["id"]
    return None

def fetch_messages(channel_id):
    result = client.conversations_history(channel=channel_id)
    return result["messages"]

def download_slack_images(messages):
    os.makedirs("data/slack_images", exist_ok=True)
    for msg in messages:
        if "files" in msg:
            for file in msg["files"]:
                if file["mimetype"].startswith("image"):
                    url = file["url_private"]
                    filename = f"data/slack_images/{file['id']}_{file['name']}"
                    headers = {"Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}"}
                    try:
                        res = requests.get(url, headers=headers)
                        if res.status_code == 200:
                            with open(filename, "wb") as f:
                                f.write(res.content)
                            print(f"Downloaded {filename}")
                    except Exception as e:
                        print(f"[WARN] Failed to download image {file['name']}: {e}")

def main():
    os.makedirs("data/slack", exist_ok=True)
    for name in CHANNEL_NAMES:
        cid = get_channel_id(name)
        if cid:
            messages = fetch_messages(cid)
            with open(f"data/slack/{name}.json", "w") as f:
                json.dump(messages, f, indent=2)
            print(f"Saved {len(messages)} messages from #{name}")
            download_slack_images(messages)
        else:
            print(f"Channel '{name}' not found")

if __name__ == "__main__":
    main()
