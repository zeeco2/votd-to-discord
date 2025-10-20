# 📖 Verse of the Day → Discord
Automatically posts the **YouVersion Bible App's Verse of the Day** to a Discord channel every morning.  
No server needed — runs 100% in **GitHub Actions** (free tier).

---

## ✨ Features
- Pulls the **daily verse** from [YouVersion Verse of the Day](https://www.bible.com/verse-of-the-day)
- Sends it straight to your **Discord channel** using a webhook
- Runs automatically every morning at the time you choose
- 100% free & serverless — no manual hosting required

---

## ⚙️ How It Works
1. **GitHub Actions** triggers the workflow daily (based on the schedule in `.github/workflows/daily.yml`).
2. The workflow runs the `votd_to_discord.py` script.
3. The script scrapes YouVersion’s Verse of the Day and posts it to your Discord channel via a webhook.

---

## 🧩 Setup Guide

### 1️⃣ Create a Discord Webhook
1. In Discord, open the channel you want to post in.  
2. Go to **Edit Channel → Integrations → Webhooks → New Webhook**.  
3. Copy the **Webhook URL** — you’ll need it for the next step.

---

### 2️⃣ Create a GitHub Repository
1. Create a new repository (public or private), e.g. `votd-to-discord`.  
2. Add these two files:
   - `votd_to_discord.py`
   - `.github/workflows/daily.yml`
3. Copy the files exactly from this repo or this README.

---

### 3️⃣ Add Your Webhook as a Secret
1. Go to your repo’s **Settings → Secrets and variables → Actions**.  
2. Click **New repository secret**.  
   - **Name:** `DISCORD_WEBHOOK_URL`  
   - **Value:** *(paste your Discord webhook URL)*  
3. Save.

---

### 4️⃣ Push Your Files
Once the files are pushed to GitHub, Actions will:
- Run automatically every day at the set time.
- You can also trigger it manually: **Actions → Verse of the Day → Run workflow**.

---

## 🕒 Adjust Posting Time
In `.github/workflows/daily.yml`, change the cron expression:
```yaml
- cron: "30 4 * * *"
