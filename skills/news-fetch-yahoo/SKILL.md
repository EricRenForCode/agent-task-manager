---
name: news-fetch-yahoo
description: Fetch and summarize recent Yahoo News articles (RSS/search) on stock-sensitive topics (solar, robotics, aerospace, semiconductors, etc.). Use when the user wants Yahoo News coverage or a structured RSS-based digest.
---

# News Fetch Yahoo

## Overview
Fetch recent Yahoo News articles for a topic, then summarize and assess potential stock impact. Prefer RSS for reliability; fall back to browser search if needed.

## Quick Start
**Inputs**
- `topic` (required)
- `time_frame` (hours, default 24)
- `limit` (default 5)

**Preferred: RSS script**
1. Run the RSS helper (category RSS + keyword filter):
   ```bash
   python3 scripts/fetch_yahoo_rss.py --category tech --topic "solar" --limit 5
   ```
2. Filter items to the last `time_frame` hours (by `pubDate`), then summarize.

**Fallback: Browser search**
- Open: `https://news.search.yahoo.com/search?p=<urlencoded_topic>`
- Extract top results (title, snippet, date, source, link), then summarize.

## Output Format (example)
1. **Title:** …
   **Summary:** …
   **Potential stock impact:** …
   **Link:** …

## Notes
- Focus on keywords: **earnings, regulation, merger, subsidy, shortage, breakthrough**.
- If fewer than `limit` items match the time window, return what is available and note the cutoff.

## Resources
- `scripts/fetch_yahoo_rss.py` — pulls Yahoo search RSS and prints items as JSON.
