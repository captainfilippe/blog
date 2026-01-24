import streamlit as st
import os
from datetime import datetime
import frontmatter

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Rota Teológica",
    page_icon="⛵",
    layout="centered"
)

# =========================
# CSS BÁSICO (LEITURA)
# =========================
st.markdown(
    """
    <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FRX42JQ16R"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FRX42JQ16R');
</script>
    """,
    unsafe_allow_html=True)


# st.markdown("""
# <style>
# .post-title {
#     font-size: 26px;
#     font-weight: 600;
#     margin-bottom: 4px;
# }
# .post-meta {
#     color: #777;
#     font-size: 14px;
#     margin-bottom: 16px;
# }
# .post-card {
#     max-width: 820px;
#     margin: auto;
#     margin-bottom: 48px;
# }
# .post-image img {
#     border-radius: 6px;
# }
# </style>
# """, unsafe_allow_html=True)

# =========================
# FUNÇÕES
# =========================
POSTS_DIR = "posts"


def load_posts():
    posts = []

    if not os.path.exists(POSTS_DIR):
        return posts

    for file in os.listdir(POSTS_DIR):
        if not file.endswith(".md"):
            continue

        path = os.path.join(POSTS_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

            # --- DATA SEGURA ---
            raw_date = post.get("date")
            try:
                date = datetime.fromisoformat(str(raw_date))
            except Exception:
                date = datetime.now()

            posts.append({
                "slug": file.replace(".md", ""),
                "title": post.get("title", "Sem título"),
                "author": post.get("author", "Autor desconhecido"),
                "date": date,
                "summary": post.get("summary", ""),
                "content": post.content,
                "tags": post.get("tags", []),
                "image": post.get("image", None)
            })

    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def go_home():
    st.session_state.pop("post", None)


# =========================
# CARREGAR POSTS
# =========================
posts = load_posts()

# =========================
# HEADER (COM VOLANTE)
# =========================
col1, col2 = st.columns([1, 8])

with col1:
    st.image("assets/capitao.jpg", width=70)

with col2:
    st.markdown("## Rota Teológica")
    st.caption("Artigos semanais sobre Escritura e teologia")
st.divider()

# =========================
# VIEW: POST INDIVIDUAL
# =========================
if "post" in st.session_state:
    slug = st.session_state["post"]
    post = next(p for p in posts if p["slug"] == slug)

    st.button("← Voltar", on_click=go_home)

    # IMAGEM DO ARTIGO
    if post["image"]:
        st.image(post["image"], use_container_width=True)

    st.markdown(f"<div class='post-title'>{post['title']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='post-meta'>{post['author']} · {post['date'].strftime('%d %b %Y')}</div>",
        unsafe_allow_html=True
    )

    st.markdown(post["content"], unsafe_allow_html=True)

    if post["tags"]:
        st.markdown("**Tags:** " + ", ".join(post["tags"]))

# =========================
# VIEW: LISTA DE POSTS (HOME)
# =========================
else:
    for post in posts:
        with st.container():
            st.markdown("<div class='post-card'>", unsafe_allow_html=True)

            # IMAGEM NO HOME
            if post["image"]:
                st.image(post["image"], use_container_width=True)

            st.markdown(f"<div class='post-title'>{post['title']}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='post-meta'>{post['author']} · {post['date'].strftime('%d %b %Y')}</div>",
                unsafe_allow_html=True
            )

            st.write(post["summary"])

            if st.button("Leia mais →", key=post["slug"]):
                st.session_state["post"] = post["slug"]

            st.markdown("</div>", unsafe_allow_html=True)


