import asyncio
import edge_tts
import requests
from bs4 import BeautifulSoup

# ===== SETTINGS =====
SUBSTACK_URL = "https://yourname.substack.com"  # Change to your Substack homepage
VOICE = "en-GB-RyanNeural"  # Try: en-GB-SoniaNeural, en-US-JennyNeural, etc.
OUTPUT_FILE = "latest_substack_narration.mp3"

def get_latest_article_text():
    # Fetch Substack homepage
    resp = requests.get(SUBSTACK_URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find latest article link
    latest_post_link = soup.find("a", {"data-testid": "post-preview-title"})
    if not latest_post_link:
        raise Exception("Could not find latest article link.")

    latest_url = latest_post_link["href"]
    if latest_url.startswith("/"):
        latest_url = SUBSTACK_URL.rstrip("/") + latest_url

    print(f"📄 Latest article URL: {latest_url}")

    # Fetch article content
    article_resp = requests.get(latest_url)
    article_soup = BeautifulSoup(article_resp.text, "html.parser")

    # Extract all text from paragraphs
    paragraphs = article_soup.find_all("p")
    text_content = "\n".join(p.get_text() for p in paragraphs)

    return text_content.strip()

async def main():
    print("🔍 Fetching latest Substack article...")
    article_text = get_latest_article_text()

    print(f"🗣 Converting article to speech ({len(article_text)} characters)...")
    communicate = edge_tts.Communicate(article_text, VOICE)
    await communicate.save(OUTPUT_FILE)

    print(f"✅ Narration saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
