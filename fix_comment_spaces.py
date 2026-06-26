#!/usr/bin/env python3
"""将书/影/音评论中间的空格替换为换行，保留末尾空格。"""

import json
import re

DATA_FILES = {
    'books': '_data/books.json',
    'films': '_data/films.json',
    'music': '_data/music.json',
}


def should_preserve(pos, text):
    """检查空格是否应保留（不转\\n）：
    1. 空格前后都是英文字母 → 保留（如 'hello world'）
    2. 空格前后都是 - 或 = → 保留（如 '- -' '= ='）
    """
    if pos <= 0 or pos >= len(text) - 1:
        return False
    before = text[pos - 1]
    after = text[pos + 1]
    # 前后都是英文字母
    if ('a' <= before <= 'z' or 'A' <= before <= 'Z') and \
       ('a' <= after <= 'z' or 'A' <= after <= 'Z'):
        return True
    # 前后都是 - 或 =
    if before in '-=' and after in '-=':
        return True
    return False


def is_eng_char(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'


def undo_false_splits(comment):
    """对于已处理过的数据，将英文-英文或 -= 的错误分段合并回去。"""
    if not comment or '\n' not in comment:
        return comment

    lines = comment.split('\n')
    merged = []
    for line in lines:
        t = line.strip('\u3000 ')
        if t:
            first_char = t[0]
            # 若当前行以英文字母开头，前一行以英文字母结尾 → 合并
            if merged and is_eng_char(first_char):
                prev_stripped = merged[-1].strip('\u3000 ')
                if prev_stripped and is_eng_char(prev_stripped[-1]):
                    merged[-1] = merged[-1].rstrip('\u3000 ') + ' ' + line.lstrip('\u3000 ')
                    continue
            # 同样规则处理 - 或 = 开头
            if merged and first_char in '-=':
                prev_stripped = merged[-1].strip('\u3000 ')
                if prev_stripped and prev_stripped[-1] in '-=':
                    merged[-1] = merged[-1].rstrip('\u3000 ') + ' ' + line.lstrip('\u3000 ')
                    continue
        merged.append(line)
    return '\n'.join(merged)


def process_comment(comment):
    """处理评论：
    - 先合并英文-英文的错误分段（undo_false_splits）
    - 中间空格 → \\n（除非前后都是英文或 -/=）
    - 每段加两个全角空格缩进（含首段）
    - 保留末尾空格。
    """
    if not comment:
        return comment

    # 先合并已处理数据的错误分段
    comment = undo_false_splits(comment)

    # 分离末尾空格
    stripped = comment.rstrip(' ')
    trailing_count = len(comment) - len(stripped)
    trailing = ' ' * trailing_count

    if not stripped:
        return trailing

    # 智能替换：空格 → \\n，但排除需保留的
    processed = re.sub(
        r' ',
        lambda m: '\n' if not should_preserve(m.start(), stripped) else ' ',
        stripped
    )

    # 所有段落加两个全角空格缩进，先去重防重复
    indent_char = '\u3000'
    parts = processed.split('\n')
    parts = [indent_char * 2 + p.lstrip(indent_char) for p in parts if p]
    processed = '\n'.join(parts)

    return processed + trailing


def process_items(items, first_n=None):
    """处理一批 items，返回修改计数。"""
    count = 0
    target = items[:first_n] if first_n else items
    for item in target:
        old = item.get('comment', '')
        new = process_comment(old)
        if old != new:
            item['comment'] = new
            count += 1
    return count


if __name__ == '__main__':
    import sys

    # 默认处理全部，可通过参数限制
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    files_to_process = sys.argv[2:] if len(sys.argv) > 2 else ['books', 'films', 'music']

    for name in files_to_process:
        path = DATA_FILES[name]
        with open(path, 'r', encoding='utf-8') as f:
            items = json.load(f)

        if name == 'books' and limit:
            n = process_items(items, first_n=limit)
        else:
            n = process_items(items)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        total = limit if (name == 'books' and limit) else len(items)
        print(f'{name}: {n}/{total} comments modified')

    print('Done.')
