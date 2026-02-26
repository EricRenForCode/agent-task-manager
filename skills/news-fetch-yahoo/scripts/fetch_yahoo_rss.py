#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
from email.utils import parsedate_to_datetime
from urllib.request import urlopen, Request
from xml.etree import ElementTree


def fetch_rss(category: str):
    url = f"https://news.yahoo.com/rss/{category}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as resp:
        data = resp.read()
    return ElementTree.fromstring(data)


def extract_items(root, topic: str | None, limit: int):
    items = []
    topic_lc = topic.lower() if topic else None
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        desc = (item.findtext("description") or "").strip()
        source = (item.findtext("source") or "").strip()

        text_blob = f"{title} {desc}".lower()
        if topic_lc and topic_lc not in text_blob:
            continue

        published_at = None
        if pub_date:
            try:
                published_at = parsedate_to_datetime(pub_date).isoformat()
            except Exception:
                published_at = pub_date

        items.append(
            {
                "title": title,
                "link": link,
                "pubDate": pub_date,
                "publishedAt": published_at,
                "description": desc,
                "source": source,
            }
        )
        if len(items) >= limit:
            break
    return items


def main():
    parser = argparse.ArgumentParser(description="Fetch Yahoo News RSS category items")
    parser.add_argument("--category", default="tech", help="rss category (e.g., tech, world, finance)")
    parser.add_argument("--topic", help="keyword filter (optional)")
    parser.add_argument("--limit", type=int, default=5, help="max items")
    args = parser.parse_args()

    try:
        root = fetch_rss(args.category)
        items = extract_items(root, args.topic, args.limit)
        print(json.dumps(items, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
