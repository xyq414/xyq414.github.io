import json, re, os

def format_content(raw):
    """Convert raw douban content to markdown with douban-style formatting."""
    # Replace literal \r\n with actual newlines
    c = raw.replace('\\r\\n', '\n').replace('\\r', '\n')
    
    # Convert numbered sections like "1、标题" to h3 headings
    # Match at line start: number + 、 + rest
    c = re.sub(r'^(\d+)、(.+)$', r'### \1、\2', c, flags=re.MULTILINE)
    
    # Convert -- divider to horizontal rule
    c = re.sub(r'^--\s*$', '---', c, flags=re.MULTILINE)
    
    # Normalize line endings
    lines = c.split('\n')
    result = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip completely empty lines
        if not stripped:
            continue
        
        # Add blank line before headings and HRs (unless at start)
        is_block = stripped.startswith('### ') or stripped == '---'
        if is_block and result:
            result.append('')
        
        result.append(stripped)
        
        # Add blank line after headings and HRs
        if is_block:
            result.append('')
    
    return '\n'.join(result) + '\n'


def make_safe_filename(title, date_str):
    """Create a safe filename from title and date."""
    # Parse date
    date_part = date_str.split(' ')[0]  # 2024-12-16
    # Keep Chinese chars and alphanumeric only, replace others with -
    safe = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title)
    safe = re.sub(r'-{2,}', '-', safe).strip('-')
    return f'{date_part}-{safe}.md'


def create_post(item, post_dir):
    """Create a _posts markdown file from an essay item."""
    title = item['title']
    date_str = item['date']
    is_status = item.get('is_status', False)
    note_url = item.get('note_url', item.get('topic_url', ''))
    
    # Format the content
    body = format_content(item.get('content', ''))
    
    # Frontmatter
    fm = [
        '---',
        'layout: post',
        f'title: "{title}"',
        'category: 杂文',
        f'date: {date_str} +0800',
        f'douban_url: {note_url}',
    ]
    if is_status:
        fm.append('is_status: true')
    fm.append('---')
    
    full = '\n'.join(fm) + '\n\n' + body
    
    filename = make_safe_filename(title, date_str)
    filepath = os.path.join(post_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full)
    
    return filename, len(full)


if __name__ == '__main__':
    post_dir = '_posts'
    os.makedirs(post_dir, exist_ok=True)
    
    with open('_data/essays.json', 'r', encoding='utf-8') as f:
        essays = json.load(f)
    
    print(f'Processing {len(essays)} essays...')
    
    for item in essays:
        fname, size = create_post(item, post_dir)
        typ = 'STATUS' if item.get('is_status') else 'NOTE'
        print(f'  [{typ}] {fname} ({size} chars)')
    
    print(f'\nDone. Created/updated {len(essays)} posts in {post_dir}/')
