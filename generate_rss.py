import os
import frontmatter
from datetime import datetime
from xml.sax.saxutils import escape

POSTS_DIR = "posts"
SITE_URL = "https://rotateologica.streamlit.app"
RSS_FILE = "rss.xml"

posts = []

for file in os.listdir(POSTS_DIR):
    if not file.endswith(".md"):
        continue

    with open(os.path.join(POSTS_DIR, file), encoding="utf-8") as f:
        post = frontmatter.load(f)

        date = datetime.fromisoformat(str(post.get("date")))

        posts.append({
            "title": post.get("title"),
            "summary": post.get("summary", ""),
            "slug": file.replace(".md", ""),
            "date": date
        })

posts.sort(key=lambda x: x["date"], reverse=True)

rss_items = ""

for post in posts[:20]:  # últimos 20
    rss_items += f"""
    <item>
      <title>{escape(post['title'])}</title>
      <link>{SITE_URL}/?post={post['slug']}</link>
      <guid>{SITE_URL}/?post={post['slug']}</guid>
      <pubDate>{post['date'].strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
      <description>{escape(post['summary'])}</description>
    </item>
    """

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Rota Teológica</title>
  <link>{SITE_URL}</link>
  <description>Artigos semanais sobre Escritura e teologia</description>
  {rss_items}
</channel>
</rss>
"""

with open(RSS_FILE, "w", encoding="utf-8") as f:
    f.write(rss)

print("rss.xml gerado com sucesso")
