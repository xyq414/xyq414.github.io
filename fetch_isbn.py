#!/usr/bin/env python3
"""从豆瓣书籍详情页爬取ISBN编号，存入books.json。"""

import json
import re
import requests
import time
import sys

COOKIE = 'dbcl2="37786310:swPjGOLvfXg"; ck=cSAs'
DATA_PATH = '_data/books.json'


def fetch_isbn(douban_url, session):
    try:
        resp = session.get(douban_url, timeout=30)
        resp.encoding = 'utf-8'
        html = resp.text
        # 在 JSON-LD 中查找: "isbn" : "9787509718087"
        m = re.search(r'"isbn"\s*:\s*"(\d{10,13})"', html)
        if m:
            return m.group(1)
        return None
    except Exception as e:
        print(f'    Error: {e}')
        return None


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        books = json.load(f)

    # 跳过已有 isbn 的
    start = 0
    for i, book in enumerate(books):
        if not book.get('isbn', ''):
            start = i
            break
    else:
        print('All books already have ISBN.')
        return

    total = sum(1 for b in books if not b.get('isbn', ''))
    print(f'Starting from index {start}, {total} missing total')

    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': COOKIE,
    })

    s.get('https://www.douban.com/', timeout=15)
    time.sleep(2)

    found = 0
    for i in range(start, len(books)):
        book = books[i]
        if book.get('isbn', ''):
            continue

        url = book.get('url', '')
        if not url:
            book['isbn'] = ''
            continue

        isbn = fetch_isbn(url, s)
        if isbn:
            book['isbn'] = isbn
            found += 1

        book['isbn'] = book.get('isbn', '') or ''

        time.sleep(1.5)

        if (i - start + 1) % 50 == 0:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(books, f, ensure_ascii=False, indent=2)
            print(f'[SAVED] processed {i+1}, found {found} new ISBN')

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    total_has = sum(1 for b in books if b.get('isbn', ''))
    print(f'\nDone. Total with ISBN: {total_has}/{len(books)}')


if __name__ == '__main__':
    main()
