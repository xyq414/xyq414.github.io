#!/usr/bin/env python3
"""抓取豆瓣书评/影评页面内容，生成 _posts/*.md 文件（使用 BeautifulSoup）。"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup

COOKIE = 'dbcl2="37786310:swPjGOLvfXg"; ck=cSAs'
BASE = 'C:/Users/xieyi/WorkBuddy/2026-06-22-13-49-21/fenwai-site'

URLS = [
    'https://book.douban.com/review/17658956/',
    'https://book.douban.com/review/17646611/',
    'https://movie.douban.com/review/17471154/',
    'https://movie.douban.com/review/17395717/',
    'https://book.douban.com/review/16766964/',
    'https://book.douban.com/review/16770490/',
    'https://book.douban.com/review/16337096/',
    'https://movie.douban.com/review/15679935/',
    'https://movie.douban.com/review/15099314/',
]


def fetch_review(session, url):
    """抓取豆瓣书评/影评页面的标题、日期、内容。"""
    r = session.get(url, timeout=30)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')

    # 标题：og:title meta 或 title tag
    title = ''
    og = soup.find('meta', property='og:title')
    if og and og.get('content'):
        title = og['content']
        if ' (评论:' in title:
            title = title.split(' (评论:')[0].strip()
    if not title:
        t = soup.find('title')
        if t:
            title = t.text.strip()
    title = title.strip()

    # 日期：从 HTML 中提取
    date_str = ''
    m = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', r.text)
    if m:
        date_str = m.group(1)

    # 内容：提取 review-content 中的 data-page 段落
    content = ''
    rc = soup.find('div', class_='review-content')
    if rc:
        paragraphs = rc.find_all('p', attrs={'data-page': True})
        parts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                parts.append(text)
        content = '\n\n'.join(parts)
    else:
        content = '(无法提取内容)'

    return title, date_str, content


def main():
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': COOKIE,
    })

    # 预热
    s.get('https://www.douban.com/', timeout=15)
    time.sleep(2)

    posts_dir = f'{BASE}/_posts'

    for i, url in enumerate(URLS):
        print(f'[{i+1}/9] {url}...', flush=True)
        title, date_str, content = fetch_review(s, url)

        if not title:
            title = f'无题-{i+1}'

        date_part = date_str[:10] if date_str else '2026-06-23'
        safe_title = title.replace('/', '-').replace(':', ' -').replace('?', '').replace('*', '').replace('"', '').replace('\\', '')
        safe_title = safe_title[:40]

        full_date = f'{date_part} 12:00:00 +0800'

        filename = f'{posts_dir}/{date_part}-{safe_title}.md'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write('layout: post\n')
            f.write(f'title: "{title}"\n')
            f.write('category: 杂文\n')
            f.write('tag: 书影评\n')
            f.write(f'date: {full_date}\n')
            f.write(f'douban_url: {url}\n')
            f.write('---\n\n')
            f.write(content)

        print(f'  → {filename.split("/")[-1]}', flush=True)
        print(f'  title: {title[:50]}', flush=True)
        print(f'  date: {date_str}', flush=True)
        print(f'  content: {len(content)} chars', flush=True)

        time.sleep(2)

    print('\nDone! 9 reviews fetched.')


if __name__ == '__main__':
    main()
