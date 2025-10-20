import os, re, requests
from bs4 import BeautifulSoup

VOTD_URL = "https://www.bible.com/verse-of-the-day"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TIMEOUT = 20

def fetch_votd():
    """
    Scrapes YouVersion's Verse of the Day page and returns (text, reference, version, link).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (+https://github.com/yourname/votd-to-discord)"
    }
    r = requests.get(VOTD_URL, headers=headers, timeout=TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # The page renders the verse text and reference in visible text.
    # We’ll detect the first long-ish scripture line and a trailing reference like "John 3:16 (NIV)".
    body_text = " ".join(soup.get_text(" ", strip=True).split())

    # Find a pattern like: "... Ephesians 2:8-9 (NIV)"
    m = re.search(r"([1-3]?\s?[A-Za-z]+\s\d+:\d+(?:-\d+)?)(?:\s*\(([^)]+)\))", body_text)
    reference, version = (m.group(1), m.group(2)) if m else ("", "")

    # Heuristic: take the verse text as the sentence(s) immediately preceding the reference
    verse_text = ""
    if m:
        ref_start = m.start()
        # Look back ~320 chars for verse text then trim to sentence boundary
        snippet = body_text[max(0, ref_start-320):ref_start].strip()
        # Clean odd joins like "... boast.Ephesians" etc.
        verse_text = re.sub(r"\s{2,}", " ", snippet).strip(" .•–—")
        # If the verse text still includes prior labels, prune common labels
        verse_text = re.sub(r"(Share\s*)+$", "", verse_text).strip()

    # Fallbacks if heuristic missed:
    if not verse_text:
        # Try a simpler capture of the first long clause before the reference
        verse_text = "Verse of the Day"

    return verse_text, reference, version, VOTD_URL

def post_to_discord(text, reference, version, link):
    if not DISCORD_WEBHOOK_URL:
        raise RuntimeError("Missing DISCORD_WEBHOOK_URL environment variable.")

    title = f"📖 Verse of the Day — {reference} {f'({version})' if version else ''}".strip()
    content = f"**{title}**\n{text}\n\nMore: {link}"

    # Basic message (you can switch to embeds if you like)
    resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": content}, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.status_code

if __name__ == "__main__":
    vt, ref, ver, link = fetch_votd()
    post_to_discord(vt, ref, ver, link)
