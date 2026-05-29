#!/usr/bin/env python3
"""
add_project.py
コマンドラインから `projects.json` に新しい作品エントリを追加します。
使い方例:
  python add_project.py --id scratch-3 --title "迷路ゲーム" --platform Scratch \
    --description "プレイヤーがゴールを目指す迷路ゲーム" --link "https://scratch.mit.edu/projects/123456789/"
"""
import argparse
import json
from pathlib import Path
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


def main():
    parser = argparse.ArgumentParser(description='projects.json にプロジェクトを追加します')
    parser.add_argument('--id', required=True, help='ユニークなID（例: scratch-3）')
    parser.add_argument('--title', required=True, help='作品のタイトル')
    parser.add_argument('--platform', required=True, help='プラットフォーム（例: Scratch, Unity）')
    parser.add_argument('--description', default='', help='短い説明')
    parser.add_argument('--link', default='', help='外部URL（任意）')
    args = parser.parse_args()

    projects = load_projects()
    # 重複チェック
    if any(p.get('id') == args.id for p in projects):
        print(f"Error: id '{args.id}' は既に存在します。別の id を指定してください。", file=sys.stderr)
        sys.exit(1)

    new = {
        'id': args.id,
        'title': args.title,
        'platform': args.platform,
        'description': args.description,
        'link': args.link,
    }
    projects.append(new)
    save_projects(projects)
    print(f"プロジェクト '{args.title}' を projects.json に追加しました。")


if __name__ == '__main__':
    main()
