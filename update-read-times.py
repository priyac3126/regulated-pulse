#!/usr/bin/env python3
"""Recalculate blog read times at 225 wpm, excluding works-cited lists and table notes."""
import re
from pathlib import Path
from html.parser import HTMLParser

WPM = 225
path = Path('index.html')
html = path.read_text(encoding='utf-8')

class ContentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.artId = None
        self.in_content = False
        self.depth = 0
        self.skip = []
        self.buf = []
        self.out = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get('class') or '').split()
        if tag == 'article' and attrs.get('id', '').startswith('post-') and attrs.get('id', '').endswith('-container'):
            self.artId = attrs['id']
            self.out.setdefault(self.artId, [])
        if not self.in_content:
            if self.artId and tag == 'div' and 'blog-post-content' in classes:
                self.in_content = True
                self.depth = 1
            return
        if tag == 'div':
            self.depth += 1
        if 'works-cited' in classes or 'table-note' in classes:
            self.skip.append(tag)
        if tag in ('p', 'h2', 'h3', 'li', 'td', 'th', 'blockquote', 'br'):
            self.buf.append(' ')
    def handle_startendtag(self, tag, attrs):
        if self.in_content and tag in ('br', 'img'):
            self.buf.append(' ')
    def handle_endtag(self, tag):
        if not self.in_content:
            if tag == 'article':
                self.artId = None
            return
        if self.skip and tag == self.skip[-1]:
            self.skip.pop()
        if tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                text = re.sub(r'\s+', ' ', ''.join(self.buf)).strip()
                self.out[self.artId].append(text)
                self.in_content = False
                self.buf = []
        if tag == 'article':
            self.artId = None
    def handle_data(self, data):
        if self.in_content and not self.skip:
            self.buf.append(data)

parser = ContentParser()
parser.feed(html)
s = html
changes = []
for article_id, chunks in parser.out.items():
    key = article_id.replace('post-', '').replace('-container', '')
    words = len(' '.join(chunks).split())
    minutes = max(1, int(words / WPM + 0.5))
    patterns = [
        r'(<article id="%s"[\s\S]{0,2000}?<p class="text-sm mb-8"[^>]*>[^<]*?·\s*)(\d+)(\s*min\s*read)' % re.escape(article_id),
        r"(id: 'post-%s'[^\n]*?date: '[^']*?· )(\d+)( min read')" % re.escape(key),
    ]
    for pattern in patterns:
        match = re.search(pattern, s)
        if match and int(match.group(2)) != minutes:
            s = s[:match.start()] + match.group(1) + str(minutes) + match.group(3) + s[match.end():]
            changes.append((key, int(match.group(2)), minutes))

    # Restrict card edits to the matching button, so cards without a read time
    # never borrow one from a later card or article.
    card_pattern = re.compile(r'<button\b(?=[^>]*\bid="card-%s-click")[\s\S]*?</button>' % re.escape(key))
    card_match = card_pattern.search(s)
    if card_match:
        block = card_match.group(0)
        updated_block, count = re.subn(
            r'(<p class="text-xs text-slate-500 font-medium">[^<]*?·\s*)(\d+)(\s*min\s*read)',
            lambda m: m.group(1) + str(minutes) + m.group(3), block, count=1)
        if count and updated_block != block:
            old_minutes = int(re.search(r'·\s*(\d+)\s*min\s*read', block).group(1))
            s = s[:card_match.start()] + updated_block + s[card_match.end():]
            changes.append((key, old_minutes, minutes))

path.write_text(s, encoding='utf-8')
print('Read times checked at', WPM, 'wpm.')
for key, old, new in changes:
    print(f'{key}: {old} -> {new} min')
if not changes:
    print('All read times are already accurate.')
