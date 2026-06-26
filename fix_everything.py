"""V4: Final fix for topic content."""
import json, re, time, os
import requests

COOKIE = 'dbcl2="37786310:swPjGOLvfXg"; ck=cSAs'
POST_DIR = '_posts'

def extract_content(html, is_topic):
    if is_topic:
        idx = html.find('topic-richtext')
        if idx < 0:
            return ''
        search_from = html.find('</div>', idx)
        end = html.find('</div>\n            </div>\n          </div>\n        </div>', search_from)
        if end < 0:
            end = html.find('</div>\n    </div>\n  </div>', search_from)
        if end < 0:
            end = html.find('<div class="topic-doc"', search_from)
        if end < 0:
            return ''
        content = html[idx:end]
        content = re.sub(r'^[^>]*>', '', content)
    else:
        for pat in [
            r'<div[^>]*id="link-report"[^>]*>(.*?)</div>\s*</div>',
            r'<div[^>]*id="link-report"[^>]*>(.*?)</div>',
        ]:
            m = re.search(pat, html, re.DOTALL)
            if m:
                content = m.group(1)
                break
        else:
            return ''
    
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'</p>', '\n\n', content)
    content = re.sub(r'<p[^>]*>', '', content)
    content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
    content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]+>', '', content)
    content = content.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
    content = content.replace('&quot;','"').replace('&#39;',"'").replace('&nbsp;',' ')
    # Clean CSS/JS
    content = re.sub(r'\.\w[\w-]*\s*\{[^}]*\}', '', content)
    content = re.sub(r'\(function\s*\([^)]*\)\s*\{.*?\}\s*\)\s*\(\s*\)', '', content, flags=re.DOTALL)
    content = re.sub(r'addEventListener\s*\([^)]*\)\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'document\.\w+', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    return content

# ── Load ──
with open('_data/essays.json', 'r', encoding='utf-8') as f:
    essays = json.load(f)

# ── Session ──
s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': COOKIE
})
try:
    s.get('https://www.douban.com/', timeout=15)
    time.sleep(1)
except: pass

# ── Fetch all ──
for i, e in enumerate(essays):
    title = e['title']
    is_status = e['is_status']
    if is_status and e.get('topic_url'):
        url = e['topic_url']
        utype = 'topic'
    elif not is_status and e.get('note_id'):
        url = f"https://www.douban.com/note/{e['note_id']}/"
        utype = 'note'
    else:
        continue
    
    old_len = len(e.get('content', ''))
    print(f'  [{i+1}] {title[:30]} ({utype}) → ', end='', flush=True)
    
    html = ''
    for _ in range(3):
        try:
            resp = s.get(url, timeout=30)
            resp.encoding = 'utf-8'
            html = resp.text
            if resp.status_code == 200: break
            time.sleep(2)
        except: time.sleep(2)
    
    if not html:
        print('FAILED')
        continue
    if '仅自己可见' in html or '你没有权限访问' in html:
        print('PRIVATE')
        e['_remove'] = True
        continue
    
    c = extract_content(html, utype == 'topic')
    if c:
        e['content'] = c
        print(f'OK {len(c)} chars (was {old_len})')
    else:
        print(f'NO CONTENT (was {old_len})')

# ── Save ──
essays = [e for e in essays if not e.get('_remove')]
with open('_data/essays.json', 'w', encoding='utf-8') as f:
    json.dump(essays, f, ensure_ascii=False, indent=2)
print(f'\n{len(essays)} essays saved.\n')

# ── Posts ──
os.makedirs(POST_DIR, exist_ok=True)
for e in essays:
    ts = e['title']
    ds = e['date']
    ct = e['content']
    is_s = e['is_status']
    nu = e.get('topic_url', e.get('note_url', ''))
    y, mon, d = ds.split(' ')[0].split('-')
    
    md = ct
    md = re.sub(r'^(\d+)、(.+)$', r'### \1、\2', md, flags=re.MULTILINE)
    md = re.sub(r'^--\s*$', '---', md, flags=re.MULTILINE)
    
    fm = f'---\nlayout: post\ntitle: "{ts}"\ncategory: 杂文\ndate: {ds} +0800\nis_status: {str(is_s).lower()}\n'
    if nu: fm += f'douban_url: {nu}\n'
    fm += '---\n\n'
    
    safe = re.sub(r'[-]{2,}', '-', ts.replace(' ', '-').replace('/', '-').replace('?', '').replace('：', '-').replace('（', '-').replace('）', '-'))
    fp = os.path.join(POST_DIR, f'{y}-{mon}-{d}-{safe}.md')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(fm + md)
    print(f'  {os.path.basename(fp)}: {len(fm)+len(md)}c, {len(md.splitlines())}l')

print('\nDone.')
