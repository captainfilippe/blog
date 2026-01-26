import streamlit as st
import os
from datetime import datetime
import frontmatter
import requests
import uuid
import markdown
from PIL import Image
# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Rota Teológica",
    page_icon="⛵",
    layout="centered"
)


MEASUREMENT_ID = "G-FRX42JQ16R"
API_SECRET = "UzllgCsCTTugrmE7114Bmg"

client_id = str(uuid.uuid4())

requests.post(
    f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}",
    json={
        "client_id": client_id,
        "events": [
            {
                "name": "page_view",
                "params": {
                    "page_title": "Rota Teológica",
                    "page_location": "https://rotateologica.streamlit.app"
                }
            }
        ]
    }
)

# =========================
# CSS BÁSICO (LEITURA)
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;700&family=Inter:wght@400;600&display=swap');

/* Títulos com fonte Serifada (mais clássico/teológico) */
.post-title {
    font-family: 'Crimson Pro', serif;
    font-size: 34px;
    color: #1a1a1a;
    line-height: 1.2;
}

/* Corpo do texto com fonte Sans-Serif (melhor leitura) */
body, .stMarkdown {
    font-family: 'Inter', sans-serif;
    color: #333;
}

/* Estilização dos Cards na Home */
div[data-testid="stVerticalBlock"] > div:has(div.post-card) {
    border-bottom: 1px solid #eee;
    padding-bottom: 2rem;
    margin-bottom: 2rem;
    width: 100px !important;
    height: 100px !important;
}

</style>
""", unsafe_allow_html=True)

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
        img = Image.open(post["image"])
        img = img.resize((600, 250))  # largura, altura
        st.image(img)

    st.markdown(f"<div class='post-title'>{post['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='post-meta'>{post['author']} · {post['date'].strftime('%d %b %Y')}</div>", unsafe_allow_html=True)

    st.markdown(post["content"], unsafe_allow_html=True)

    if post["tags"]:
        st.markdown("**Tags:** " + ", ".join(post["tags"]))

# =========================
# VIEW: LISTA DE POSTS (HOME)
# =========================
else:
    # Cria colunas: 2 posts por linha
    for i in range(0, len(posts), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(posts):
                post = posts[i + j]
                with cols[j]:
                    if post["image"]:
                        img = Image.open(post["image"])
                        img = img.resize((600, 250))  # largura, altura
                        st.image(img)
                    st.markdown(f"<div class='post-title' style='font-size:20px;'>{post['title']}</div>", unsafe_allow_html=True)
                    #st.markdown(f"<div class='post-meta'>{post['author']} · {post['date'].strftime('%d %b %Y')}</div>", unsafe_allow_html=True)
                    st.caption(f"{post['author']} · {post['date'].strftime('%d %b %Y')}")
                    st.write(post["summary"][:100] + "...") # Resumo curto
                    if st.button("Leia mais", key=post["slug"]):
                        st.session_state["post"] = post["slug"]
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# with st.sidebar:
#     st.image("assets/capitao.jpg", width=100)
#     st.markdown("### Sobre o Rota")
#     #st.info("Navegando pelas águas profundas da teologia reformada e estudos bíblicos.")
    
#     st.divider()
 
#python -m streamlit run streamlit_app.py --server.address=10.18.206.58 --server.port=8510
