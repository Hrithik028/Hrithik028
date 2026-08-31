#!/usr/bin/env python3
"""Refresh the repository-hosted GitHub profile statistics SVG."""

from __future__ import annotations

import json
import os
import re
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path


USERNAME = os.environ.get("PROFILE_USERNAME", "Hrithik028")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "assets" / "github-stats.svg"
README_PATH = ROOT / "README.md"


def request_json(url: str, *, payload: dict | None = None) -> dict | list:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-stats-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_stats() -> tuple[dict, list[tuple[str, int]]]:
    profile = request_json(f"https://api.github.com/users/{USERNAME}")
    repos = request_json(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    )
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar { totalContributions }
        }
      }
    }
    """
    graphql = request_json(
        "https://api.github.com/graphql",
        payload={"query": query, "variables": {"login": USERNAME}},
    )
    if "errors" in graphql:
        raise RuntimeError(f"GitHub GraphQL error: {graphql['errors']}")

    language_counts = Counter(
        repo["language"] for repo in repos if repo.get("language")
    )
    stats = {
        "public_repos": int(profile["public_repos"]),
        "followers": int(profile["followers"]),
        "following": int(profile["following"]),
        "contributions": int(
            graphql["data"]["user"]["contributionsCollection"]
            ["contributionCalendar"]["totalContributions"]
        ),
    }
    return stats, language_counts.most_common(4)


def render_language_rows(languages: list[tuple[str, int]]) -> str:
    colors = ["#3976d6", "#d7b35c", "#8eb8ff", "#8b1e2d"]
    max_count = max((count for _, count in languages), default=1)
    rows = []
    for index, (language, count) in enumerate(languages):
        column = index // 2
        row = index % 2
        x = 32 + (column * 545)
        y = 270 + (row * 42)
        label_width = 170
        bar_width = max(36, round(285 * count / max_count))
        rows.append(
            f'<text x="{x}" y="{y}" fill="#f4ead5" font-size="14">'
            f'{escape(language.upper())}</text>'
            f'<rect x="{x + label_width}" y="{y - 12}" width="{bar_width}" '
            f'height="14" rx="7" fill="{colors[index]}"/>'
            f'<text x="{x + label_width + bar_width + 12}" y="{y}" '
            f'fill="#b8c6dd" font-size="13">{count} repos</text>'
        )
    return "".join(rows)


def render_svg(stats: dict, languages: list[tuple[str, int]], stamp: str) -> str:
    language_rows = render_language_rows(languages)
    cards = [
        ("PUBLIC REPOSITORIES", stats["public_repos"], "#d7b35c"),
        ("CONTRIBUTIONS", stats["contributions"], "#3976d6"),
        ("FOLLOWERS", stats["followers"], "#8b1e2d"),
        ("FOLLOWING", stats["following"], "#d7b35c"),
    ]
    card_markup = []
    for index, (label, value, accent) in enumerate(cards):
        x = 32 + (index * 262)
        width = 244 if index < 3 else 250
        card_markup.append(
            f'<g transform="translate({x} 102)"><rect width="{width}" height="91" '
            f'rx="8" fill="#02050b" stroke="#234d99"/>'
            f'<text x="20" y="30" fill="#8eb8ff" font-size="13" '
            f'letter-spacing="2">{label}</text>'
            f'<text x="20" y="72" fill="#f4ead5" font-size="37" '
            f'font-weight="700">{value}</text>'
            f'<path d="M165 68h54" stroke="{accent}" stroke-width="3" '
            f'filter="url(#glow)"/></g>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="360" viewBox="0 0 1100 360" role="img" aria-labelledby="title desc">
  <title id="title">{escape(USERNAME)} GitHub statistics snapshot</title>
  <desc id="desc">A themed GitHub statistics panel showing {stats['public_repos']} public repositories, {stats['contributions']} contributions, {stats['followers']} followers, and {stats['following']} following.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07152d"/><stop offset="1" stop-color="#02050b"/></linearGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="1" y="1" width="1098" height="358" rx="14" fill="url(#bg)" stroke="#d7b35c" stroke-opacity=".55" stroke-width="2"/>
  <path d="M28 74H1072" stroke="#3976d6" stroke-opacity=".45"/>
  <g font-family="Consolas, monospace">
    <text x="32" y="43" fill="#d7b35c" font-size="19" letter-spacing="4">GITHUB TELEMETRY // {escape(USERNAME.upper())}</text>
    <text x="1068" y="43" fill="#8eb8ff" font-size="13" text-anchor="end">VERIFIED SNAPSHOT · {stamp}</text>
    {''.join(card_markup)}
    <text x="32" y="235" fill="#d7b35c" font-size="14" letter-spacing="3">PUBLIC REPOSITORY LANGUAGE DISTRIBUTION</text>
    {language_rows}
    <text x="1068" y="334" fill="#7f91ae" font-size="12" text-anchor="end">Updated automatically by GitHub Actions</text>
  </g>
</svg>
'''


def update_readme(display_date: str) -> None:
    content = README_PATH.read_text(encoding="utf-8")
    updated, replacements = re.subn(
        r"> Snapshot generated from public GitHub data on \*\*[^*]+\*\*\.",
        f"> Snapshot generated from public GitHub data on **{display_date}**.",
        content,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError("README snapshot date marker was not found exactly once")
    README_PATH.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN or GH_TOKEN is required")
    stats, languages = fetch_stats()
    now = datetime.now(timezone.utc)
    svg_stamp = now.strftime("%d %b %Y").upper()
    display_date = f"{now.day} {now.strftime('%B %Y')}"
    SVG_PATH.write_text(render_svg(stats, languages, svg_stamp), encoding="utf-8", newline="\n")
    update_readme(display_date)
    print(
        f"Updated {SVG_PATH.relative_to(ROOT)}: "
        f"{stats['public_repos']} repos, {stats['contributions']} contributions, "
        f"{stats['followers']} followers"
    )


if __name__ == "__main__":
    main()
