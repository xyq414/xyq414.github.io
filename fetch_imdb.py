#!/usr/bin/env python3
"""从豆瓣电影详情页爬取IMDb编号，存入films.json（支持断点续爬）。"""

import json
import re
import requests
import time
import sys

COOKIE = 'dbcl2="37786310:swPjGOLvfXg"; ck=cSAs'
DATA_PATH = '_data/films.json'
SAVE_INTERVAL = 50  # 每50条存一次


def fetch_imdb(douban_url, session):
    try:
        resp = session.get(douban_url, timeout=30)
        resp.encoding = 'utf-8'
        html = resp.text
        m = re.search(r'<span class="pl">IMDb:</span>\s*(\w+)', html)
        if m:
            return m.group(1)
        m = re.search(r'imdb\.com/title/(tt\d+)', html)
        return m.group(1) if m else None
    except Exception as e:
        print(f'    Error: {e}')
        return None


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        films = json.load(f)

    # 找到第一个没有 imdb 字段（或为空）的索引
    start = 0
    for i, film in enumerate(films):
        if not film.get('imdb', ''):
            start = i
            break
    else:
        print('All films already have IMDb.')
        return

    total_missing = sum(1 for ff in films if not ff.get('imdb', ''))
    print(f'Starting from index {start}, {total_missing} missing total')

    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': COOKIE,
    })

    # 预热
    s.get('https://www.douban.com/', timeout=15)
    time.sleep(2)

    count = 0
    last_save = 0
    for i in range(start, len(films)):
        film = films[i]
        if film.get('imdb', ''):
            continue  # 已爬过跳过

        url = film.get('url', '')
        if not url:
            film['imdb'] = ''
            continue

        print(f'[{i+1}/{len(films)}] {film["title"][:30]}...', end=' ')
        sys.stdout.flush()

        imdb_id = fetch_imdb(url, s)
        if imdb_id:
            film['imdb'] = imdb_id
            count += 1
            print(f'IMDb: {imdb_id}')
        else:
            film['imdb'] = ''
            print('no IMDb')

        time.sleep(1.5)

        # 每 N 条保存一次进度
        if count > 0 and count % SAVE_INTERVAL == 0 and count != last_save:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(films, f, ensure_ascii=False, indent=2)
            last_save = count
            print(f'  [Saved at {count} found / {i+1} processed]')

    # 最终保存
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(films, f, ensure_ascii=False, indent=2)

    total = sum(1 for ff in films if ff.get('imdb', ''))
    print(f'\nDone. Total with IMDb: {total}/{len(films)}')


if __name__ == '__main__':
    main()
