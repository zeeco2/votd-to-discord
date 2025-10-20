import os
import requests
from bs4 import BeautifulSoup

# --- CONFIG ---
BIBLE_VERSION = "AMP"  # Amplified Bible
BASE_URL = "https://www.bible.com/bible"
VOTD_URL = "https://www.bible.com/verse-of-the-day"
TIMEOUT = 20

def fetch_votd():
    """Scrape YouVersion's Verse of the Day and format it neatly."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(VOTD_URL, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # The verse text is usually inside <meta property="og:description">
    verse_meta = soup.find("meta", property="og:description")
    verse_text = verse_meta["content"] if verse_meta else "Verse not found."

    # Reference (e.g. Ephesians 2:8-9)
    ref_meta = soup.find("meta", property="og:title")
    reference = ref_meta["content"].split("—")[-1].strip() if ref_meta else "Reference unavailable"

    # Build AMP link (YouVersion uses numeric IDs, but we’ll keep to VOTD_URL)
    verse_link = VOTD_URL

    return verse_text, reference, verse_link


def post_to_discord(webhook_url, verse_text, reference, verse_link):
    """Send a clean embedded message to Discord."""
    embed = {
        "title": f"📖 Verse of the Day — {reference} ({BIBLE_VERSION})",
        "description": f"_{verse_text}_",
        "url": verse_link,
        "color": 0x2ECC71,  # soft green accent
        "footer": {"text": "Powered by YouVersion Bible App"},
    }

    payload = {"embeds": [embed]}

    r = requests.post(webhook_url, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r.status_code


if __name__ == "__main__":
    verse_text, reference, verse_link = fetch_votd()

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("Missing DISCORD_WEBHOOK_URL environment variable.")

    post_to_discord(webhook_url, verse_text, reference, verse_link)

    # Optional: send to second webhook if configured
    webhook_url2 = os.environ.get("DISCORD_WEBHOOK_URL_2")
    if webhook_url2:
        post_to_discord(webhook_url2, verse_text, reference, verse_link)

