from pathlib import Path
import re, json, html
root=Path('.')
s=(root/'index.html').read_text()
posts=[
('post-battlefield','Beyond the Battlefield','The Toll of PTSD and the Fight to Improve Veteran Mental Health','Book Insights','2026-11-01'),
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
@media(min-width:2200px){html{font-size:17px}}@media(min-width:2600px){html{font-size:18px}}@media(min-width:3000px){html{font-size:19px}}@media(min-width:3400px){html{font-size:20px}}
@media(max-width:640px){.static-header{padding:1rem}.static-main{padding:2rem 1rem}.static-footer{padding-left:1rem;padding-right:1rem}.static-nav{font-size:.74rem;gap:.7rem}}
'''
(root/'article-static.css').write_text(css)
for pid,title,subtitle,cat,date in posts:
    m=re.search(r'<article id="'+re.escape(pid)+r'-container"[^>]*>(.*?)</article>',s,re.S)
    if not m:
        print('MISS',pid); continue
    inner=m.group(1)
    # strip the comment form block
    cut=inner.find('<div class="mt-16 rounded-2xl')
    if cut!=-1: inner=inner[:cut]
    inner=inner.strip().replace('src="./', 'src="/').replace("src='./", "src='/")
    if 'loading=' not in inner and '<img' in inner:
        inner=inner.replace('<img', '<img loading="lazy" decoding="async"')
    url=f'https://theregulatedpulse.com/{pid}'
    img_m=re.search(r'<img[^>]+src="([^"]+)"', inner, re.S)
    og_image=('https://theregulatedpulse.com'+img_m.group(1)) if img_m and img_m.group(1).startswith('/') else 'https://theregulatedpulse.com/preview-image-light.jpeg'
    desc=html.escape(subtitle,quote=True)
    ld={"@context":"https://schema.org","@type":"BlogPosting","headline":title,"description":subtitle,"datePublished":date,"author":{"@type":"Person","name":"Priya Chaudhari"},"publisher":{"@type":"Organization","name":"The Regulated Pulse"},"mainEntityOfPage":url}
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
<script type="application/ld+json">{json.dumps(ld,separators=(',',':'))}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="/favicon-dark.svg">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
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
</main>
<footer class="static-footer">
  <p>Read the interactive version with comments, highlights, and audio: <a href="/#post-{pid.replace('post-','')}">open article</a>.</p>
  <p>&copy; 2026 The Regulated Pulse · <a href="/">Home</a> · <a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a></p>
</footer>
</body>
</html>'''
    d=root/pid
    d.mkdir(exist_ok=True)
    page='\n'.join(line.rstrip() for line in page.splitlines()) + '\n'
    (d/'index.html').write_text(page)
    print('wrote',d/'index.html')
