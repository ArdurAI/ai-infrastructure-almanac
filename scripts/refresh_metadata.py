#!/usr/bin/env python3
"""
Refresh Metadata — Update GitHub metadata for every tool on the roster.

Usage:
    python refresh_metadata.py          # Refresh all tools
    python refresh_metadata.py --dry-run  # Show what would change

This script:
1. Reads data/roster.json
2. For each tool with a GitHub URL, fetches stars, last push date, and release info
3. Updates the roster with new metadata
4. Writes a summary of changes
"""

import argparse
import json
import logging
import os
import re
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('refresh_metadata')


def load_roster(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def save_roster(path: str, roster: dict) -> None:
    with open(path, 'w') as f:
        json.dump(roster, f, indent=2)


def parse_github_url(url: str) -> tuple:
    """Extract owner/repo from a GitHub URL."""
    if not url or 'github.com' not in url:
        return None, None
    match = re.match(r'https?://github\.com/([^/]+)/([^/]+)', url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def simulate_github_api(owner: str, repo: str) -> dict:
    """
    Simulated GitHub API fetch.
    In production, this would use the GitHub REST API with a token.
    Returns stars, last_push, and release_count.
    """
    # Simulated values — in production, fetch from https://api.github.com/repos/{owner}/{repo}
    return {
        'stars': 0,  # placeholder
        'last_push': datetime.now(timezone.utc).isoformat(),
        'release_count': 0,
        'open_issues': 0,
        'open_prs': 0,
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'simulated': True
    }


def refresh_tool_metadata(tool: dict, dry_run: bool = False) -> dict:
    """Refresh metadata for a single tool. Returns the updated tool dict."""
    # In a real implementation, we'd fetch GitHub API data here
    # For now, we simulate the structure
    github_url = tool.get('github_url', '')
    owner, repo = parse_github_url(github_url)

    if not owner or not repo:
        logger.debug(f"Skipping {tool['name']}: no GitHub URL")
        return tool

    meta = simulate_github_api(owner, repo)

    if not dry_run:
        tool['github_metadata'] = meta
        tool['last_refreshed'] = datetime.now(timezone.utc).isoformat()

    return tool


def main():
    parser = argparse.ArgumentParser(description='Refresh GitHub metadata for the roster')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--roster', default='../data/roster.json', help='Path to roster.json')
    parser.add_argument('--category', help='Only refresh a specific category')
    args = parser.parse_args()

    roster_path = os.path.join(os.path.dirname(__file__), args.roster)
    roster = load_roster(roster_path)

    total_tools = 0
    refreshed = 0

    for cat_key, category in roster['categories'].items():
        if args.category and cat_key != args.category:
            continue
        for tool in category['tools']:
            total_tools += 1
            refresh_tool_metadata(tool, dry_run=args.dry_run)
            refreshed += 1

    # Update meta
    roster['meta']['generated_at'] = datetime.now(timezone.utc).isoformat()
    roster['meta']['version'] = datetime.now(timezone.utc).strftime('%Y-%m')

    if not args.dry_run:
        save_roster(roster_path, roster)
        logger.info(f"Roster updated: {refreshed} tools refreshed, {total_tools} total")
    else:
        logger.info(f"DRY RUN: Would refresh {refreshed} tools, {total_tools} total")


if __name__ == '__main__':
    main()
