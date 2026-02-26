---
name: news-fetch-x
description: Fetch recent, high-impact news or posts from X (Twitter) about stock-sensitive topics (solar, robotics, aerospace, semiconductors, etc.). Use when a user asks for “latest X posts/news”, “hot takes”, or “stock-impacting updates” from X within a time window.
---

# News Fetch X

## Overview
Fetch and summarize recent X posts for a topic, focusing on items that could move stocks. Return a concise digest with links and potential impact.

## Quick Start
**Inputs**
- `topic` (required): e.g., “solar energy stocks”, “semiconductor shortage”
- `time_frame` (hours, default 24)
- `limit` (default 5)

**Workflow**
1. **Compute start_date** as UTC date = now − `time_frame` hours.
   ```bash
   python3 - <<'PY'
   import datetime
   hours = 24
   print((datetime.datetime.utcnow() - datetime.timedelta(hours=hours)).strftime('%Y-%m-%d'))
   PY
   ```
2. **Open X search** (live feed):
   ```
   https://twitter.com/search?q=<urlencoded_topic>%20since:<start_date>&src=typed_query&f=live
   ```
3. **Parse top posts**: capture title/content, author, date, and engagement (likes/retweets/replies). Prefer posts with **engagement ≥ 100**; if not enough results, relax to ≥ 50.
4. **Summarize** each item:
   - `Title:` short headline
   - `Summary:` 1–2 sentences
   - `Potential stock impact:` brief analysis (e.g., “positive for TSLA / ENPH / FSLR”).
5. **Return** a list of 1–`limit` items with links.

## Output Format (example)
1. **Title:** …
   **Summary:** …
   **Potential stock impact:** …
   **Link:** …

## Notes
- Prioritize items mentioning **earnings, regulation, mergers, supply constraints, subsidies, or breakthroughs**.
- If X requires login, mention the limitation and suggest Yahoo or RSS alternatives.
