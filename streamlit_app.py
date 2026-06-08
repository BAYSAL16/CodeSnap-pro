import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name
from github_loader import GitHubLoader

# ── Sayfa ayarları ──
st.set_page_config(
    page_title="CodeSnap Pro",
    page_icon="📸",
    layout="wide"
)

# ── Başlık ──
st.title("📸 CodeSnap Pro")
st.caption("Kodunu güzel PNG resimlerine dönüştür")

# ── Sidebar ayarlar ──
with st.sidebar:
    st.header("⚙️ Ayarlar")

    dil = st.selectbox("Dil", ["python", "javascript", "java", "cpp", "html", "css"])

    tema = st.selectbox("Tema", ["monokai", "dracula", "github-dark", "solarized-dark", "nord"])

    png_stili = st.radio("PNG Stili", ["🎨 Temalı", "🌈 Degrade", "⬜ Sade"])

    font_boyutu = st.slider("Font Boyutu", min_value=12, max_value=24, value=16)

    st.divider()

    st.header("🐙 GitHub'dan Yükle")
    repo_url = st.text_input("Repo URL", placeholder="https://github.com/kullanici/repo")

    if st.button("Dosyaları Listele"):
        if repo_url:
            try:
                loader = GitHubLoader()
                owner, repo_name, files = loader.get_files(repo_url)
                st.session_state["github_owner"] = owner
                st.session_state["github_repo"] = repo_name
                st.session_state["github_files"] = files
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Lütfen bir repo URL'si girin!")

    if "github_files" in st.session_state:
        secilen_dosya = st.selectbox("Dosya Seç", st.session_state["github_files"])
        if st.button("Dosyayı Yükle"):
            try:
                loader = GitHubLoader()
                content = loader.get_file_content(
                    st.session_state["github_owner"],
                    st.session_state["github_repo"],
                    secilen_dosya
                )
                st.session_state["kod"] = content
                st.success(f"✅ {secilen_dosya} yüklendi!")
            except ValueError as e:
                st.error(str(e))

# ── Ana alan ──
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("✏️ Kod Gir")

    # GitHub'dan yüklendiyse textbox'a yaz
    baslangic_kodu = st.session_state.get("kod", "# Kodunu buraya yaz\ndef merhaba():\n    print('Merhaba Dünya!')")

    kod = st.text_area(
        "Kod",
        value=baslangic_kodu,
        height=400,
        label_visibility="collapsed"
    )

    # Dosya yükleme
    yuklenen_dosya = st.file_uploader("veya dosya yükle", type=["py", "js", "java", "cpp", "html", "css"])
    if yuklenen_dosya:
        kod = yuklenen_dosya.read().decode("utf-8")
        st.session_state["kod"] = kod

with col2:
    st.subheader("👁️ Önizleme & İndir")

    if st.button("📸 Ekran Görüntüsü Al", type="primary", use_container_width=True):
        if not kod.strip():
            st.warning("Lütfen bir kod girin!")
        else:
            try:
                with st.spinner("PNG oluşturuluyor..."):

                    # Pygments ImageFormatter ile direkt PNG üret
                    lexer = get_lexer_by_name(dil)

                    if png_stili == "🎨 Temalı":
                        formatter = ImageFormatter(
                            style=tema,
                            font_size=font_boyutu,
                            line_numbers=True,
                            line_pad=5
                        )
                        img_bytes = highlight(kod, lexer, formatter)
                        img = Image.open(BytesIO(img_bytes))

                    elif png_stili == "🌈 Degrade":
                        # Önce temalı PNG üret
                        formatter = ImageFormatter(
                            style=tema,
                            font_size=font_boyutu,
                            line_numbers=True,
                            line_pad=5
                        )
                        img_bytes = highlight(kod, lexer, formatter)
                        kod_img = Image.open(BytesIO(img_bytes))

                        # Degrade arka plan oluştur
                        padding = 60
                        w = kod_img.width + padding * 2
                        h = kod_img.height + padding * 2

                        bg = Image.new("RGB", (w, h))
                        for y in range(h):
                            oran = y / h
                            r = int(102 + (118 - 102) * oran)
                            g = int(126 + (75 - 126) * oran)
                            b = int(234 + (162 - 234) * oran)
                            for x in range(w):
                                bg.putpixel((x, y), (r, g, b))

                        bg.paste(kod_img, (padding, padding))
                        img = bg

                    else:  # Sade
                        formatter = ImageFormatter(
                            style="bw",
                            font_size=font_boyutu,
                            line_numbers=True,
                            line_pad=5
                        )
                        img_bytes = highlight(kod, lexer, formatter)
                        img = Image.open(BytesIO(img_bytes))

                    # Önizleme göster
                    st.image(img, use_container_width=True)

                    # İndirme butonu
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    buf.seek(0)

                    st.download_button(
                        label="⬇️ PNG İndir",
                        data=buf,
                        file_name=f"codesnap_{dil}.png",
                        mime="image/png",
                        use_container_width=True
                    )

                    st.success("✅ Hazır! İndir butonuna bas.")

            except Exception as e:
                st.error(f"Hata: {str(e)}")