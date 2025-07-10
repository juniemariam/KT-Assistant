# fetch confluence pages
import os
from atlassian import Confluence
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

confluence = Confluence(
    url="https://sjsu-team-syncwell.atlassian.net/wiki",
    username="junie.mariamvarghese@sjsu.edu",
    password=os.getenv("CONFLUENCE_API_TOKEN")
)

# Set your page ID here
page_id = "163978"

# Fetch the page by ID
page = confluence.get_page_by_id(page_id, expand="body.storage")
html = page["body"]["storage"]["value"]
title = page["title"]
text = BeautifulSoup(html, "html.parser").get_text()

# Save the page text
os.makedirs("data/confluence", exist_ok=True)
file_path = f"data/confluence/{title.replace(' ', '_')}.txt"
with open(file_path, "w") as f:
    f.write(text)

print(f" Confluence page '{title}' saved to {file_path}")
