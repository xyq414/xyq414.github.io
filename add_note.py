"""
Add a Douban note or topic to the essays collection.
Usage: python add_note.py <douban_url>
Examples:
  python add_note.py https://www.douban.com/note/868695501/
  python add_note.py https://www.douban.com/topic/475599701/
"""
import json, re, time, requests, sys, os
from bs4 import BeautifulSoup, NavigableString, Tag

COOKIE = 'dbcl2="37786310:swPjGOLvfXg"; ck=cSAs'
POST_DIR = '_posts'


def html_to_markdown(html_str):
    """Convert HTML content to clean Markdown, preserving embedded newlines."""
    soup = BeautifulSoup(html_str, 'html.parser')

    def process_element(el):
        if isinstance(el, NavigableString):
            text = str(el)
            text = text.replace('\r', '')
            text = re.sub(r'[ \t]+', ' ', text)
            return text
        elif isinstance(el, Tag):
            tag_name = el.name.lower()
            if tag_name == 'br':
                return '\n'
            children_text = []
            for child in el.children:
                child_text = process_element(child)
                if child_text is not None:
                    children_text.append(child_text)
            text = ''.join(children_text)
            if tag_name in ('strong', 'b'):
                return f'**{text}**'
            elif tag_name in ('em', 'i'):
                return f'*{text}*'
            elif tag_name == 'u':
                return f'<u>{text}</u>'
            elif tag_name == 'span':
                style = el.get('style', '')
                if 'text-decoration: underline' in style or 'text-decoration:underline' in style:
                    return f'<u>{text}</u>'
                return text
            elif tag_name in ('p', 'div', 'section'):
                return '\n\n' + text.strip() + '\n\n'
            elif tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                level = int(tag_name[1])
                return '\n\n' + '#' * level + ' ' + text.strip() + '\n\n'
            elif tag_name == 'a':
                href = el.get('href', '')
                if href and 'doubanapp' not in href:
                    return f'[{text}]({href})'
                return text
            elif tag_name in ('script', 'style', 'noscript'):
                return ''
            else:
                return text

    text = process_element(soup)
    text = text.replace('\r', '')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return text


def extract_topic_content(soup):
    """Extract content from a Douban topic page."""
    content_div = soup.select_one('div.rich-content.topic-richtext')
    if not content_div:
        content_div = soup.select_one('div.topic-richtext')
    if not content_div:
        return ''

    inner_html = ''.join(str(child) for child in content_div.children)
    if not inner_html.strip():
        return ''

    text = html_to_markdown(inner_html)

    # Cut before UI junk markers
    junk_markers = ['\n修改\n', '\n删除\n', '\n投诉',
                    'window.createReportButton', 'var rec_url',
                    '\n赞\n', '\n转发\n', '\n微信扫码\n',
                    '\n新浪微博\n', '\nQQ好友\n', '\nQQ空间\n',
                    '来自 豆瓣App']
    min_pos = len(text)
    for marker in junk_markers:
        pos = text.find(marker)
        if pos > 0 and pos < min_pos:
            min_pos = pos
    if min_pos < len(text):
        text = text[:min_pos].rstrip()

    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'\bwindow\.\w+\([^)]*\)[;]?', '', text)
    text = re.sub(r'document\.\w+[^;]*;', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_note_content(soup):
    """Extract content from a Douban note page."""
    link_report = soup.select_one('#link-report')
    if not link_report:
        return ''

    for junk_div in link_report.select('#link-report_note'):
        junk_div.decompose()
    for junk in link_report.select('style, script, link[rel="stylesheet"]'):
        junk.decompose()

    note_div = link_report.select_one('div.note')
    if note_div:
        for app_link in note_div.select('a[href*="doubanapp"]'):
            app_link.decompose()
        for via_span in note_div.select('span.via, .from-app'):
            via_span.decompose()
        inner_html = ''.join(str(child) for child in note_div.children)
    else:
        inner_html = ''.join(str(child) for child in link_report.children)

    if not inner_html.strip():
        return ''

    text = html_to_markdown(inner_html)
    text = re.sub(r'来自\s*豆瓣\s*App\s*', '', text)
    text = re.sub(r'来自\s*$', '', text)
    text = re.sub(r'\.\w[\w-]*\s*\{[^}]*\}', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def fetch_article(url):
    """Fetch a Douban note or topic page and extract content."""
    # Determine type
    note_match = re.search(r'/note/(\d+)', url)
    topic_match = re.search(r'/topic/(\d+)', url)

    if note_match:
        article_id = note_match.group(1)
        is_status = False
        full_url = f'https://www.douban.com/note/{article_id}/'
    elif topic_match:
        article_id = topic_match.group(1)
        is_status = True
        full_url = f'https://www.douban.com/topic/{article_id}/'
    else:
        print('ERROR: URL must be a douban note or topic URL')
        return None

    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': COOKIE
    })

    print('Warming up session...')
    try:
        s.get('https://www.douban.com/', timeout=15)
        time.sleep(1)
    except:
        pass

    print(f'Fetching {full_url}...')
    resp = s.get(full_url, timeout=30)
    resp.encoding = 'utf-8'
    html = resp.text

    if '仅自己可见' in html or '你没有权限访问' in html:
        print(f'ERROR: Article is private or inaccessible')
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Title
    title_tag = soup.select_one('h1')
    title = 'Untitled'
    if title_tag:
        title = title_tag.get_text(strip=True)

    # Date
    date = '2025-01-01 00:00:00'
    date_m = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', html)
    if date_m:
        date = date_m.group(1)

    # Content
    if is_status:
        content = extract_topic_content(soup)
    else:
        content = extract_note_content(soup)

    result = {
        'title': title,
        'date': date,
        'content': content,
        'is_status': is_status,
    }

    if is_status:
        result['topic_url'] = full_url
    else:
        result['note_id'] = article_id
        result['note_url'] = full_url

    return result


def save_post(item, post_dir=POST_DIR):
    """Generate a _posts markdown file."""
    title = item['title']
    date_str = item['date']
    body = item['content']

    fm = [
        '---',
        'layout: post',
        f'title: "{title}"',
        'category: 杂文',
        f'date: {date_str} +0800',
    ]
    if item.get('is_status'):
        fm.append('is_status: true')
        fm.append(f'douban_url: {item.get("topic_url", "")}')
    else:
        fm.append(f'douban_url: {item.get("note_url", "")}')
    fm.append('---')

    # Format body
    md = body
    md = re.sub(r'^(\d+)、(.+)$', r'### \1、\2', md, flags=re.MULTILINE)

    full = '\n'.join(fm) + '\n\n' + md

    date_part = date_str.split(' ')[0]
    safe = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title)
    safe = re.sub(r'-{2,}', '-', safe).strip('-')
    filename = f'{date_part}-{safe}.md'
    filepath = os.path.join(post_dir, filename)

    os.makedirs(post_dir, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full)

    return filepath


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python add_note.py <douban_url>')
        print('Examples:')
        print('  python add_note.py https://www.douban.com/note/868695501/')
        print('  python add_note.py https://www.douban.com/topic/475599701/')
        sys.exit(1)

    url = sys.argv[1]
    article = fetch_article(url)
    if article is None:
        sys.exit(1)

    print(f'Title: {article["title"]}')
    print(f'Date: {article["date"]}')
    print(f'Content: {len(article["content"])} chars')
    print(f'Type: {"Status (topic)" if article["is_status"] else "Note"}')

    # Save to essays.json
    json_path = os.path.join('_data', 'essays.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        essays = json.load(f)

    # Check for duplicate by title
    existing = [e for e in essays if e.get('title') == article['title']]
    if existing:
        print(f'Article "{article["title"]}" already exists. Updating content.')
        essays = [e for e in essays if e.get('title') != article['title']]

    essays.append(article)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(essays, f, ensure_ascii=False, indent=2)

    # Generate _post
    post_path = save_post(article)
    print(f'Post saved: {post_path}')
    print(f'Total essays: {len(essays)}')
    print('Done! Ready to commit and push.')
