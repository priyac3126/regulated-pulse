from pathlib import Path
import re, json, html
root=Path('.')
s=(root/'index.html').read_text()
posts=[
('post-battlefield','Beyond the Battlefield','The Toll of PTSD and the Fight to Improve Veteran Mental Health','Book Insights','2026-11-07'),
('post-farmer','“Equity is the Only Acceptable Goal”','The Enduring Legacy of Paul Farmer','Book Insights','2026-11-26'),
('post-art-cure','The Fifth Pillar: Why the Arts Belong in Clinical Care','How arts engagement can improve patient outcomes','Book Insights','2026-10-25'),
('post-malpractice','State Medical Malpractice Laws Comparison','Texas and Arizona','Law & Policy','2026-07-01'),
('post-cdc-interview','From Anatomy Labs to Biosafety Laws','An Interview with CDC Attorney Taylor Revenew','Interview','2026-07-01'),
('post-book-recs','Book Recommendations','My top 10 heathcare reads','Reading List','2026-06-01'),
('post-compassion','The Case for Compassionate Care','The medical necessity of compassionate care','Book Insights','2026-06-01'),
('post-migration','Healing Without Borders','Bridging gaps in migrant health through innovation and policy','Book Insights','2026-06-01'),
('post-na','"If You Knew the Conditions"','The evolution of Native American health care','History & Policy','2026-06-01'),
('post-giant-leap','A Giant Leap: Trust and Oversight in Healthcare AI','AI will transform healthcare. This book explains why and what it means for healthtech regulation.','Book Insights','2026-06-01'),
('post-ai','Beyond Compliance: The Intersection of AI, Inclusive UI/UX, and Digital Rights','How we build ethical, inclusive design','AI & Policy','2026-06-01'),
('post-welcome','Welcome to The Regulated Pulse','What to expect from the blog','Welcome','2026-06-01'),
('post-pain-brokers','The Pain Brokers','Defective healthcare technology and legal corruption','Reading List','2026-07-30'),
('post-med-ed','The State of Medical Education','Medical knowledge doubles every few months','Education','2026-06-01'),
('post-epic','Stifled Innovation','The Cost of Monopolized Electronic Health Records','Industry','2026-06-01'),
('post-quote-spotlight','Quote Spotlight','Any sufficiently advanced technology is indistinguishable from magic.','Inspiration','2026-06-01'),
]
css='''
:root{--bg:#080b11;--surface:#0b1220;--border:#1f2937;--text:#f1f5f9;--muted:#9fadc1;--accent:#75c1fa}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:'Plus Jakarta Sans',ui-sans-serif,sans-serif;line-height:1.7}
a{color:var(--accent)}
.static-header{max-width:none;margin:0 auto;padding:1rem 2rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--bg);z-index:20}
.static-brand{display:flex;align-items:center;gap:.75rem;color:var(--text);text-decoration:none}
.static-brand svg{width:36px;height:36px}
.static-brand small{display:block;color:var(--accent);font-size:9px;letter-spacing:.18em;text-transform:uppercase}
.static-brand strong{display:block;font-family:'Playfair Display',Georgia,serif;font-size:1.1rem;line-height:1.1}
.static-nav{display:flex;gap:1rem;font-size:.82rem;font-weight:600;flex-wrap:wrap}
.static-nav a{color:var(--muted);text-decoration:none}
.static-nav a:hover{color:var(--accent)}
.static-main{max-width:50rem;margin:0 auto;padding:3rem 2rem 4rem}
.static-kicker{font-family:'Plus Jakarta Sans',sans-serif;font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin-bottom:1rem}
.static-article h2{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(2rem,5vw,3rem);line-height:1.12;margin:0 0 .4rem;color:var(--text)}
.static-article h3{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(1.1rem,2vw,1.35rem);font-weight:600;line-height:1.35;margin:0 0 1rem;color:#cbd5e1}
.static-article .meta{font-size:.8rem;color:#fecdd3;margin-bottom:2rem}
.static-article .blog-post-content{font-family:'Source Serif 4',Georgia,serif;font-size:1.08rem;color:#cbd5e1}
.static-article .blog-post-content p{margin:0 0 1.2rem}
.static-article .blog-post-content h2,.static-article .blog-post-content h3{color:var(--text);margin:2rem 0 .75rem}
.static-article .blog-post-content a{color:var(--accent)}
.static-article .blog-post-content blockquote{margin:1.75rem 0;padding:.25rem 0 .25rem 1.25rem;border-left:3px solid var(--accent);font-style:italic;color:#dbe4f0}
.static-article .blog-post-content cite{display:block;margin-top:.6rem;font-size:.82rem;color:var(--muted)}
img{max-width:100%;height:auto}
.static-article img{border-radius:.4rem}
.static-article .comparison-table{width:100%;border-collapse:collapse;margin:1.5rem 0;font-family:'Plus Jakarta Sans',sans-serif;font-size:1em;display:table}
.static-article .comparison-table th,.static-article .comparison-table td{border:1px solid #475569;padding:.55rem .65rem;vertical-align:top;white-space:normal}
.static-article .comparison-table th{background:#1e293b;color:var(--text);text-align:left}
.static-article .comparison-table .group-row td{background:#111b2c;color:var(--text);font-weight:700;text-transform:uppercase;font-size:.78em;letter-spacing:.05em}
.static-article .comparison-table p{margin:0 0 .5rem;font-size:inherit}
.static-article .blog-post-content p.pulse-motto{font-size:1.21rem}
.static-article .pulse-motto-accent{color:var(--accent)}
.static-article .works-cited{font-size:.86rem;color:var(--muted)}
.static-article .works-cited li{margin-bottom:.6rem}
.static-article .table-note{font-size:.8rem;color:var(--muted)}
.static-article .img-a11y-desc{font-size:.7rem;color:var(--muted)}
.static-footer{max-width:50rem;margin:0 auto;padding:0 2rem 3rem;color:#7f8fa6;font-size:.78rem;border-top:1px solid var(--border);padding-top:1.5rem}
.static-footer a{color:var(--accent)}

@media(max-width:700px){
.static-article .comparison-table{display:block;overflow-x:visible;white-space:normal}
.static-article .comparison-table thead{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.static-article .comparison-table tbody,.static-article .comparison-table tr,.static-article .comparison-table td{display:block;width:100%}
.static-article .comparison-table tr{border:1px solid #475569;border-radius:.35rem;margin-bottom:1rem;overflow:hidden}
.static-article .comparison-table td{border:0;border-bottom:1px solid #475569;padding:1rem}
.static-article .comparison-table tr td:last-child{border-bottom:0}
.static-article .comparison-table td::before{content:attr(data-label);display:block;margin-bottom:.45rem;color:var(--accent);font-family:'Plus Jakarta Sans',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.static-article .comparison-table .group-row td::before{content:none}
.static-article .comparison-table .group-row td{border-bottom:0}
}
.static-article-nav{display:flex;justify-content:space-between;gap:1rem;max-width:50rem;margin:1rem auto 2rem;padding:0 2rem;font-size:.85rem}
.static-article-nav a{color:var(--accent);text-decoration:none;max-width:48%}
.static-article-nav .next{margin-left:auto;text-align:right}
@media(min-width:2200px){html{font-size:17px}}@media(min-width:2600px){html{font-size:18px}}@media(min-width:3000px){html{font-size:19px}}@media(min-width:3400px){html{font-size:20px}}
@media(max-width:640px){.static-header{padding:1rem}.static-main{padding:2rem 1rem}.static-footer{padding-left:1rem;padding-right:1rem}.static-nav{font-size:.74rem;gap:.7rem}}
'''
(root/'article-static.css').write_text(css)
for pid,title,subtitle,cat,date in posts:
    m=re.search(r'<article id="'+re.escape(pid)+r'-container"[^>]*>(.*?)</article>',s,re.S)
    if not m:
        print('MISS',pid); continue
    inner=m.group(1)
    nav_posts=sorted(posts,key=lambda post: post[4],reverse=True)
    nav_index=[post[0] for post in nav_posts].index(pid)
    nav_parts=[]
    if nav_index>0:
        newer=nav_posts[nav_index-1]
        nav_parts.append('<a href="/'+newer[0]+'">&larr; '+html.escape(newer[1])+'</a>')
    else:
        nav_parts.append('<span></span>')
    if nav_index<len(nav_posts)-1:
        older=nav_posts[nav_index+1]
        nav_parts.append('<a class="next" href="/'+older[0]+'">'+html.escape(older[1])+' &rarr;</a>')
    article_nav=''.join(nav_parts)
    # strip the comment form block
    cut=inner.find('<div class="mt-16 rounded-2xl')
    if cut!=-1: inner=inner[:cut]
    inner=inner.strip().replace('src="./', 'src="/').replace("src='./", "src='/")
    if 'loading=' not in inner and '<img' in inner:
        inner=inner.replace('<img', '<img loading="lazy" decoding="async"')
    url=f'https://theregulatedpulse.com/{pid}'
    img_m=re.search(r'<img[^>]+src="([^"]+)"', inner, re.S)
    og_image='https://theregulatedpulse.com/og/'+pid+'.jpg'
    desc=html.escape(subtitle,quote=True)
    blog_ld={"@type":"BlogPosting","headline":title,"description":subtitle,"datePublished":date,"author":{"@type":"Person","name":"Priya Chaudhari"},"publisher":{"@type":"Organization","name":"The Regulated Pulse"},"mainEntityOfPage":url}
    crumb_ld={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://theregulatedpulse.com/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://theregulatedpulse.com/#blog"},{"@type":"ListItem","position":3,"name":title,"item":url}]}
    ld={"@context":"https://schema.org","@graph":[blog_ld,crumb_ld]}
    page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} · The Regulated Pulse</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)} · The Regulated Pulse">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)} · The Regulated Pulse">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="alternate" type="application/rss+xml" title="The Regulated Pulse" href="https://theregulatedpulse.com/feed.xml">
<link rel="alternate" type="application/rss+xml" title="The Regulated Pulse Podcast" href="https://theregulatedpulse.com/podcast-feed.xml">
<script type="application/ld+json">{json.dumps(ld,separators=(',',':'))}</script>
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="icon" type="image/svg+xml" href="/favicon-dark.svg">
<link rel="stylesheet" href="/pulse-tailwind.css">
<link rel="stylesheet" href="/article-static.css">
</head>
<body>
<header class="static-header">
  <a class="static-brand" href="/">
    <svg viewBox="0 0 160 160" fill="none" aria-hidden="true"><polyline points="20,80 40,80 50,50 60,110 70,80 80,80 85,65 90,95 100,80 120,80 140,80" stroke="#75c1fa" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <span><small>Health &amp; Tech Law</small><strong>The Regulated Pulse</strong></span>
  </a>
  <nav class="static-nav"><a href="/">Blog</a><a href="/#podcast">Podcast</a><a href="/#about">About Me</a><a href="/feed.xml">RSS</a></nav>
</header>
<main class="static-main">
  <article class="static-article">
    <div class="static-kicker">{html.escape(cat)}</div>
    {inner}
  </article>
  <nav class="static-article-nav" aria-label="Article navigation">{article_nav}</nav>
</main>
<footer class="static-footer">
  <p>Read the interactive version with comments, highlights, and audio: <a href="/#post-{pid.replace('post-','')}">open article</a>.</p>
  <p>&copy; 2026 The Regulated Pulse · <a href="/">Home</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></p>
</footer>
</body>
</html>'''
    table_js = """<script>document.querySelectorAll('.comparison-table').forEach(table=>{const headers=Array.from(table.querySelectorAll('thead th')).map(th=>th.textContent.trim());table.querySelectorAll('tbody tr').forEach(row=>{if(row.classList.contains('group-row'))return;Array.from(row.children).forEach((cell,i)=>{if(headers[i]&&!cell.getAttribute('data-label'))cell.setAttribute('data-label',headers[i]);});});});</script>"""
    page = page.replace('</body>', table_js + '\n</body>')
    d=root/pid
    d.mkdir(exist_ok=True)
    page='\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
    (d/'index.html').write_text(page)
    print('wrote',d/'index.html')

# Generate the RSS feed and sitemap from the same post metadata used for pages.
from datetime import datetime, timezone
from email.utils import format_datetime

def rfc_date(iso):
    return format_datetime(datetime.fromisoformat(iso).replace(hour=12, tzinfo=timezone.utc))

updates = {'post-book-recs': '2026-11-26'}
ordered = sorted(posts, key=lambda post: updates.get(post[0], post[4]), reverse=True)
items = []
for pid, title, subtitle, cat, date in ordered:
    items.append('''    <item>
      <title>''' + html.escape(title) + '''</title>
      <link>https://theregulatedpulse.com/''' + pid + '''</link>
      <guid isPermaLink="true">https://theregulatedpulse.com/''' + pid + '''</guid>
      <description>''' + html.escape(subtitle) + '''</description>
      <pubDate>''' + rfc_date(date) + '''</pubDate>
    </item>''')
latest = max(updates.get(pid, date) for pid, title, subtitle, cat, date in posts)
feed = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Regulated Pulse</title>
    <link>https://theregulatedpulse.com/</link>
    <atom:link href="https://theregulatedpulse.com/feed.xml" rel="self" type="application/rss+xml" />
    <description>Healthcare, technology, law, and policy.</description>
    <language>en-us</language>
    <lastBuildDate>''' + rfc_date(latest) + '''</lastBuildDate>
''' + '\n'.join(items) + '''
  </channel>
</rss>
'''
(root/'feed.xml').write_text(feed)

urls = [('https://theregulatedpulse.com/', latest, 'weekly', '1.0'),
        ('https://theregulatedpulse.com/terms.html', latest, 'yearly', '0.3'),
        ('https://theregulatedpulse.com/privacy.html', latest, 'yearly', '0.3')]
for pid, title, subtitle, cat, date in ordered:
    urls.append(('https://theregulatedpulse.com/' + pid, updates.get(pid, date), 'monthly', '0.8'))
url_entries = []
for loc, lastmod, freq, priority in urls:
    url_entries.append('  <url>\n    <loc>' + loc + '</loc>\n    <lastmod>' + lastmod + '</lastmod>\n    <changefreq>' + freq + '</changefreq>\n    <priority>' + priority + '</priority>\n  </url>')
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(url_entries) + '\n</urlset>\n'
(root/'sitemap.xml').write_text(sitemap)

# Episode update feed. Episode pages remain on the interactive site; no audio
# enclosure is invented because the hosted platforms own the actual media files.
episodes = []
catalog = s[s.index('const PODCAST_EP_CATALOG = ['):]
catalog = catalog[:catalog.index('];')]
for match in re.finditer(r"\{\s*id: '(ep\d+)'[\s\S]*?title: '([^']+)'[\s\S]*?dur: '([^']+)'[\s\S]*?date: '([^']+)'[\s\S]*?spotifyUrl: '([^']+)'", catalog):
    eid, title, dur, date, url = match.groups()
    episodes.append((eid, title, dur, date, url))
episode_items = []
for eid, title, dur, date, url in episodes:
    iso_date = datetime.strptime(date, '%B %Y').strftime('%Y-%m-01')
    episode_items.append('''    <item>
      <title>''' + html.escape(title) + '''</title>
      <link>''' + html.escape(url, quote=True) + '''</link>
      <guid isPermaLink="false">''' + eid + '''</guid>
      <description>The Regulated Pulse Podcast · ''' + eid + ''' · ''' + dur + ''' · ''' + date + '''</description>
      <pubDate>''' + rfc_date(iso_date) + '''</pubDate>
    </item>''')
podcast_feed = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Regulated Pulse Podcast</title>
    <link>https://theregulatedpulse.com/#podcast</link>
    <atom:link href="https://theregulatedpulse.com/podcast-feed.xml" rel="self" type="application/rss+xml" />
    <description>Conversations at the intersection of healthcare, technology, law, leadership, and the human experience.</description>
    <language>en-us</language>
    <lastBuildDate>''' + rfc_date(latest) + '''</lastBuildDate>
''' + '\n'.join(episode_items) + '''
  </channel>
</rss>
'''
(root/'podcast-feed.xml').write_text(podcast_feed)
print('wrote feed.xml, sitemap.xml, podcast-feed.xml')
