#!/usr/bin/env python3
"""Publish a count-free, recent-country feed from GoatCounter statistics."""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


SITE_CODE = os.environ.get("GOATCOUNTER_SITE_CODE", "jaizanuar")
API_TOKEN = os.environ.get("GOATCOUNTER_API_TOKEN", "")
OUTPUT_PATH = pathlib.Path("data/reader-countries.json")
MAX_COUNTRIES = 25


def iso_hour(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat().replace("+00:00", "Z")


def api_get(path: str, query: Optional[dict[str, object]] = None) -> dict:
    url = f"https://{SITE_CODE}.goatcounter.com/api/v0/{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "jaizanuar.com-country-feed/1.0",
    })

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def first_hit_date(today: dt.date) -> dt.date:
    payload = api_get("sites")
    site = next((item for item in payload.get("sites", []) if item.get("code") == SITE_CODE), None)
    if not site:
        raise RuntimeError(f"GoatCounter site {SITE_CODE!r} was not found")

    timestamp = site.get("first_hit_at") or site.get("created_at")
    if not timestamp:
        return today
    return dt.datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).date()


def day_locations(day: dt.date, now: dt.datetime) -> list[dict[str, str]]:
    start = dt.datetime.combine(day, dt.time.min, tzinfo=dt.timezone.utc)
    next_day = start + dt.timedelta(days=1)
    end = min(next_day, now)
    if end <= start:
        return []

    payload = api_get("stats/locations", {
        "start": iso_hour(start),
        "end": iso_hour(end),
        "limit": 100,
    })

    locations = []
    for location in payload.get("stats", []):
        code = str(location.get("id", "")).split("-", 1)[0].upper()
        name = str(location.get("name", "")).strip()
        if len(code) == 2 and code.isalpha() and name and name != "(unknown)":
            locations.append({"code": code, "name": name})
    return locations


def collect_recent_countries(now: dt.datetime) -> list[dict[str, str]]:
    countries: list[dict[str, str]] = []
    seen: set[str] = set()

    earliest_day = first_hit_date(now.date())
    day = now.date()
    while day >= earliest_day:
        for country in day_locations(day, now):
            if country["code"] not in seen:
                seen.add(country["code"])
                countries.append(country)
                if len(countries) == MAX_COUNTRIES:
                    return countries
        time.sleep(0.12)
        day -= dt.timedelta(days=1)

    return countries


def main() -> int:
    if not API_TOKEN:
        print("GOATCOUNTER_API_TOKEN is required", file=sys.stderr)
        return 2

    try:
        countries = collect_recent_countries(dt.datetime.now(dt.timezone.utc))
    except urllib.error.HTTPError as error:
        print(f"GoatCounter API returned HTTP {error.code}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"Could not reach GoatCounter: {error}", file=sys.stderr)
        return 1
    except (RuntimeError, ValueError) as error:
        print(f"Could not determine GoatCounter history: {error}", file=sys.stderr)
        return 1

    current = {}
    if OUTPUT_PATH.exists():
        current = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))

    payload = {"countries": countries}
    if current == payload:
        print("Reader-country order is unchanged")
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Published {len(countries)} unique reader countries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
