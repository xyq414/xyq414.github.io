"""
Fix all essay content by re-fetching from Douban and properly cleaning UI junk.
V2: Uses BeautifulSoup for robust extraction.
"""
import json, re, time, os
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

COOKIE = 'your_douban_cookie_here'  # 替换为你的豆瓣 Cookie
POST_DIR = '_posts'
DATA_FILE = '_data/essays.json'

def html_to_markdown(html_str):
    """Convert HTML content to clean Markdown, handling bold, underline, paragraphs.
    
    Key: preserves embedded newlines in text (Douban notes often use real \\n for paragraphs
    inside a single <p> tag, not <br> tags)."""
    soup = BeautifulSoup(html_str, 'html.parser')
    
    def process_element(el):
        if isinstance(el, NavigableString):
            text = str(el)
            # Replace carriage returns, but KEEP embedded newlines
            # (Douban notes often have paragraphs with real \\n inside a single <p>)
            text = text.replace('\r', '')
            # Collapse runs of spaces/tabs (but NOT newlines)
            text = re.sub(r'[ \t]+', ' ', text)
            return text
        elif isinstance(el, Tag):
            tag_name = el.name.lower()
            
            if tag_name == 'br':
                return '\n'
            
            # Collect children text
            children_text = []
            for child in el.children:
                child_text = process_element(child)
                if child_text is not None:
                    children_text.append(child_text)
            
            text = ''.join(children_text)
            
            # Handle styling
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
                # Wrap in double newlines for paragraph boundary
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
    
    # Clean up
    text = text.replace('\r', '')
    # Collapse 3+ consecutive newlines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove any HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    
    return text


def extract_topic_content(soup):
    """Extract content from a Douban topic page."""
    # Find the rich-content topic-richtext div
    content_div = soup.select_one('div.rich-content.topic-richtext')
    if not content_div:
        content_div = soup.select_one('div.topic-richtext')
    if not content_div:
        return ''
    
    # Get the inner HTML (all child elements but not the div itself)
    inner_html = ''.join(str(child) for child in content_div.children)
    
    if not inner_html.strip():
        return ''
    
    # Convert to markdown
    text = html_to_markdown(inner_html)
    
    # Remove trailing junk patterns
    # Anything after common end markers that indicate UI elements
    junk_markers = [
        '\n修改\n', '\n删除\n', '\n投诉',
        'window.createReportButton',
        'var rec_url', 'addEventListener',
        '\n赞\n', '\n转发\n',
        '\n微信扫码\n', '\n新浪微博\n', '\nQQ好友\n', '\nQQ空间\n',
        '来自 豆瓣App',
    ]
    
    # Find the earliest junk marker
    min_pos = len(text)
    for marker in junk_markers:
        pos = text.find(marker)
        if pos > 0 and pos < min_pos:
            min_pos = pos
    
    if min_pos < len(text):
        text = text[:min_pos].rstrip()
    
    # Additional cleanup: remove any remaining HTML tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    
    # Remove iframe-like JS patterns
    text = re.sub(r'\bwindow\.\w+\([^)]*\)[;]?', '', text)
    text = re.sub(r'document\.\w+[^;]*;', '', text)
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text


def extract_note_content(soup):
    """Extract content from a Douban note page."""
    # Find the link-report div
    link_report = soup.select_one('#link-report')
    if not link_report:
        return ''
    
    # Remove the "来自 豆瓣App" section (link-report_note div)
    for junk_div in link_report.select('#link-report_note'):
        junk_div.decompose()
    
    # Remove CSS and JS blocks
    for junk in link_report.select('style, script, link[rel="stylesheet"]'):
        junk.decompose()
    
    # Find the actual note content div
    note_div = link_report.select_one('div.note')
    if note_div:
        # Remove the "来自 豆瓣App" text that may be at the end of the note div
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
    
    # Clean up "来自 豆瓣App" variants
    text = re.sub(r'来自\s*豆瓣\s*App\s*', '', text)
    text = re.sub(r'来自\s*$', '', text)
    
    # Remove any CSS blocks that leaked through
    text = re.sub(r'\.\w[\w-]*\s*\{[^}]*\}', '', text)
    
    # Collapse whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text


def main():
    # Load essays
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        essays = json.load(f)
    
    # Set up session
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
    
    # Fetch each article
    for i, e in enumerate(essays):
        title = e['title']
        is_status = e['is_status']
        
        if is_status and e.get('topic_url'):
            url = e['topic_url']
        elif not is_status and e.get('note_id'):
            url = f"https://www.douban.com/note/{e['note_id']}/"
        else:
            print(f'  [{i+1}] {title[:30]} → SKIP (no URL)')
            continue
        
        old_len = len(e.get('content', ''))
        print(f'  [{i+1}] {title[:30]} ({url[-30:]}) → ', end='', flush=True)
        
        html = ''
        for attempt in range(3):
            try:
                resp = s.get(url, timeout=30)
                resp.encoding = 'utf-8'
                html = resp.text
                if resp.status_code == 200:
                    break
                time.sleep(2)
            except Exception as ex:
                print(f'retry({attempt}) ', end='', flush=True)
                time.sleep(2)
        
        if not html:
            print('FAILED')
            continue
        
        if '仅自己可见' in html or '你没有权限访问' in html:
            print('PRIVATE → removing')
            e['_remove'] = True
            continue
        
        soup = BeautifulSoup(html, 'html.parser')
        
        if is_status:
            content = extract_topic_content(soup)
        else:
            content = extract_note_content(soup)
        
        if content:
            # Additional cleanup: remove any trailing blank paragraphs
            content = re.sub(r'\n+$', '', content)
            e['content'] = content
            delta = len(content) - old_len
            sign = '+' if delta > 0 else ''
            if delta != 0:
                print(f'OK {len(content)}c ({sign}{delta})')
            else:
                print(f'OK {len(content)}c (unchanged)')
        else:
            print(f'NO CONTENT extracted (was {old_len}c) → keeping old')
    
    # Remove private articles
    removed = [e['title'] for e in essays if e.get('_remove')]
    essays = [e for e in essays if not e.get('_remove')]
    
    # Save essays.json
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(essays, f, ensure_ascii=False, indent=2)
    print(f'\n{len(essays)} essays saved to {DATA_FILE}')
    if removed:
        print(f'Removed: {removed}')
    
    # Generate _posts
    os.makedirs(POST_DIR, exist_ok=True)
    for e in essays:
        ts = e['title']
        ds = e['date']
        ct = e['content']
        is_s = e['is_status']
        
        if is_s:
            nu = e.get('topic_url', '')
        else:
            nu = e.get('note_url', '')
        
        y, mon, d = ds.split(' ')[0].split('-')
        
        # Format content for Jekyll
        md = ct
        
        # Convert numbered sections (1、xxx) to ### headings
        md = re.sub(r'^(\d+)、(.+)$', r'### \1、\2', md, flags=re.MULTILINE)
        
        # Build frontmatter
        fm = f'---\nlayout: post\ntitle: "{ts}"\ncategory: 杂文\ndate: {ds} +0800\nis_status: {str(is_s).lower()}\n'
        if nu:
            fm += f'douban_url: {nu}\n'
        fm += '---\n\n'
        
        safe_name = re.sub(r'[-]{2,}', '-', ts.replace(' ', '-').replace('/', '-').replace('?', '').replace('：', '-').replace('（', '-').replace('）', '-'))
        fp = os.path.join(POST_DIR, f'{y}-{mon}-{d}-{safe_name}.md')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(fm + md)
        print(f'  {os.path.basename(fp)}: {len(md.splitlines())} lines, {len(fm)+len(md)} chars')
    
    print('\nDone. All posts regenerated.')


if __name__ == '__main__':
    main()
