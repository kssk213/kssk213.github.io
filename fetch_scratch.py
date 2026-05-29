#!/usr/bin/env python3
"""
fetch_scratch.py
Scratch のユーザー名からプロジェクト一覧を取得して `projects.json` に追記します。
使い方:
  python fetch_scratch.py --username kssk213
"""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import sys

HERE = Path(__file__).resolve().parent
PROJECTS_FILE = HERE / 'projects.json'


def load_projects():
    if not PROJECTS_FILE.exists():
        return []
    with PROJECTS_FILE.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_projects(projects):
    with PROJECTS_FILE.open('w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
        f.write('\n')


def fetch_projects_for_user(username):
    url = f'https://api.scratch.mit.edu/users/{username}/projects'
    req = Request(url, headers={'User-Agent': 'fetch-scratch-script'})
    try:
        with urlopen(req, timeout=15) as resp:
            data = resp.read().decode('utf-8')
            return json.loads(data)
    except HTTPError as e:
        print(f'HTTP error: {e.code} {e.reason}', file=sys.stderr)
        return []
    except URLError as e:
        print(f'URL error: {e.reason}', file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description='Fetch Scratch projects and add to projects.json')
    parser.add_argument('--username', required=True, help='Scratch username')
    args = parser.parse_args()

    projects = load_projects()
    existing_ids = {p.get('id') for p in projects}

    fetched = fetch_projects_for_user(args.username)
    if not fetched:
        print('No projects fetched or fetch failed.', file=sys.stderr)
        sys.exit(1)

    added = 0
    for p in fetched:
        pid = p.get('id')
        if pid is None:
            continue
        new_id = f'scratch-{pid}'
        if new_id in existing_ids:
            continue
        title = p.get('title') or f'project-{pid}'
        desc = p.get('description') or ''
        link = f'https://scratch.mit.edu/projects/{pid}/'
        projects.append({
            'id': new_id,
            'title': title,
            'platform': 'Scratch',
            'description': desc,
            'link': link,
        })
        existing_ids.add(new_id)
        added += 1

    if added:
        save_projects(projects)
        print(f'Added {added} new project(s) to projects.json')
    else:
        print('No new projects to add')


if __name__ == '__main__':
    main()
