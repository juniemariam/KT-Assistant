# parsing the images in slack images
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import mimetypes

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

IMAGE_DIR = "data/slack_images"
OUTPUT_FILE = "data/slack_image_chunks.jsonl"
os.makedirs("data", exist_ok=True)

chunks = []

def summarize_image(image_path):
    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type and mime_type.startswith("image"):
            image = Image.open(image_path)
            prompt = "This is a screenshot shared in Slack. Summarize what it contains in a way that could help future developers understand its relevance."
            response = model.generate_content([prompt, image])
            return response.text
    except Exception as e:
        print(f" Failed to summarize {image_path}: {str(e)}")
        return None

for fname in os.listdir(IMAGE_DIR):
    path = os.path.join(IMAGE_DIR, fname)
    if path.lower().endswith((".png", ".jpg", ".jpeg")):
        print(f" Processing {fname}...")
        summary = summarize_image(path)
        if summary:
            chunks.append({
                "source": "slack-image",
                "file": fname,
                "content": summary
            })

with open(OUTPUT_FILE, "w") as f:
    for chunk in chunks:
        json.dump(chunk, f)
        f.write("\n")

print(f" Summarized {len(chunks)} images → {OUTPUT_FILE}")
