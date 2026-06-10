import streamlit as st
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from github_loader import GitHubLoader

# ── Sayfa ayarları ──
st.set_page_config(
    page_title="CodeSnap Pro",
    page_icon="🌸",
    layout="wide"
)

# ── GIF'i base64'e çevir ──
def get_gif_base64():
    try:
        with open("Animated_GIF.gif", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

gif_base64 = get_gif_base64()
gif_html = f'<img src="data:image/gif;base64,{gif_base64}" style="width:100%;border-radius:12px;"/>' if gif_base64 else ""

# ── CSS ──
st.markdown(f"""
<style>
    /* Ana arka plan */
    .stApp {{
        background: linear-gradient(160deg, #0a0a1a 0%, #0d0d2b 40%, #1a0a2e 100%);
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(10, 10, 30, 0.97);
        border-right: 1px solid #ff9eb544;
    }}

    /* Typewriter başlık */
    .main-title {{
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #ff9eb5, #c084fc, #ff9eb5);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: typewriter 2s steps(20, end), gradientShift 4s ease infinite 2s;
        overflow: hidden;
        white-space: nowrap;
        margin: 0 auto;
        width: fit-content;
    }}

    @keyframes typewriter {{
        from {{ width: 0; }}
        to {{ width: 100%; }}
    }}

    @keyframes gradientShift {{
        0% {{ background-position: 0% center; }}
        50% {{ background-position: 100% center; }}
        100% {{ background-position: 0% center; }}
    }}

    .sub-title {{
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #c084fc88;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 1s ease-in 2s both;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Butonlar */
    .stButton > button {{
        background: linear-gradient(135deg, #2d1b4e, #3d1f6e);
        color: #ff9eb5;
        border: 1px solid #ff9eb544;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, #ff9eb5, #c084fc);
        color: #0a0a1a;
        border-color: #ff9eb5;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px #ff9eb555, 0 0 40px #c084fc22;
    }}

    /* Text area */
    .stTextArea textarea {{
        background: #0d0d2b !important;
        color: #e2d9f3 !important;
        border: 1px solid #ff9eb533 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}

    .stTextArea textarea:focus {{
        border-color: #ff9eb5 !important;
        box-shadow: 0 0 15px #ff9eb522 !important;
    }}

    /* Selectbox */
    .stSelectbox > div > div {{
        background: #0d0d2b !important;
        color: #e2d9f3 !important;
        border: 1px solid #ff9eb533 !important;
        transition: all 0.3s ease;
    }}

    /* Label */
    label, [data-testid="stSidebar"] label {{
        color: #c084fc !important;
        font-family: 'Courier New', monospace !important;
    }}

    /* Bölüm başlıkları */
    .section-header {{
        font-family: 'Courier New', monospace;
        color: #ff9eb5;
        font-size: 1.1rem;
        border-bottom: 1px solid #ff9eb533;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-in;
    }}

    /* Download butonu */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #ff9eb5, #c084fc) !important;
        color: #0a0a1a !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        animation: downloadPulse 2s ease-in-out infinite;
    }}

    @keyframes downloadPulse {{
        0%, 100% {{ box-shadow: 0 0 10px #ff9eb544; }}
        50% {{ box-shadow: 0 0 25px #ff9eb588, 0 0 50px #c084fc33; }}
    }}

    /* Resim fade-in */
    [data-testid="stImage"] {{
        animation: imageFadeIn 0.8s ease-out;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(255, 158, 181, 0.15);
    }}

    @keyframes imageFadeIn {{
        from {{ opacity: 0; transform: scale(0.95) translateY(20px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    /* Success */
    .stSuccess {{
        animation: fadeIn 0.5s ease-in;
        border-left: 3px solid #ff9eb5 !important;
    }}

    /* Error shake */
    .stAlert {{
        animation: shake 0.5s ease-in-out;
    }}

    @keyframes shake {{
        0%, 100% {{ transform: translateX(0); }}
        25% {{ transform: translateX(-5px); }}
        75% {{ transform: translateX(5px); }}
    }}

    /* Radio */
    .stRadio label {{
        color: #c084fc !important;
        font-family: 'Courier New', monospace !important;
        transition: color 0.3s ease;
    }}

    .stRadio label:hover {{
        color: #ff9eb5 !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: #0a0a1a; }}
    ::-webkit-scrollbar-thumb {{ background: #ff9eb566; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #ff9eb5; }}

    /* Divider */
    hr {{ border-color: #ff9eb522 !important; }}

    /* Yaprak animasyonu */
    .sakura-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
    }}

    .petal {{
        position: absolute;
        top: -20px;
        font-size: 16px;
        animation: fall linear infinite;
        opacity: 0.7;
    }}

    @keyframes fall {{
        0% {{ top: -20px; transform: rotate(0deg) translateX(0); opacity: 0.8; }}
        50% {{ transform: rotate(180deg) translateX(30px); }}
        100% {{ top: 100vh; transform: rotate(360deg) translateX(-20px); opacity: 0; }}
    }}
</style>

<!-- Yaprak yağmuru -->
<div class="sakura-container" id="sakura"></div>
<script>
    const container = document.getElementById('sakura');
    const petals = ['🌸', '🌺', '✿', '❀'];
    for (let i = 0; i < 15; i++) {{
        const petal = document.createElement('div');
        petal.className = 'petal';
        petal.innerHTML = petals[Math.floor(Math.random() * petals.length)];
        petal.style.left = Math.random() * 100 + 'vw';
        petal.style.animationDuration = (Math.random() * 6 + 6) + 's';
        petal.style.animationDelay = (Math.random() * 8) + 's';
        petal.style.fontSize = (Math.random() * 12 + 10) + 'px';
        container.appendChild(petal);
    }}
</script>
""", unsafe_allow_html=True)


def hex_to_rgb(hex_color):
    hex_color = hex_color.strip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c*2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def kod_to_png(kod, dil, tema, stil, font_boyutu=15):
    lexer = get_lexer_by_name(dil)
    style_obj = get_style_by_name(tema)
    bg_color = style_obj.background_color or "#1a1a2e"
    default_color = "#e2d9f3"

    satirlar = kod.split("\n")
    satir_sayisi = len(satirlar)
    en_uzun = max(len(s) for s in satirlar) if satirlar else 40

    char_w = font_boyutu * 0.6
    char_h = font_boyutu * 1.6
    padding = 40
    satir_no_genislik = 50

    img_w = int(padding * 2 + satir_no_genislik + en_uzun * char_w)
    img_h = int(padding * 2 + satir_sayisi * char_h + 40)
    img_w = max(img_w, 600)

    if stil == "🌈 Degrade":
        img = Image.new("RGB", (img_w + 80, img_h + 80))
        draw = ImageDraw.Draw(img)
        for y in range(img_h + 80):
            oran = y / (img_h + 80)
            r = int(255 * oran + 10 * (1 - oran))
            g = int(158 * oran + 10 * (1 - oran))
            b = int(181 * (1 - oran) + 46 * oran)
            draw.line([(0, y), (img_w + 80, y)], fill=(r, g, b))
        kart = Image.new("RGB", (img_w, img_h), hex_to_rgb(bg_color))
        img.paste(kart, (40, 40))
        draw = ImageDraw.Draw(img)
        offset_x, offset_y = 40, 40

    elif stil == "⬜ Sade":
        img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        bg_color = "#ffffff"
        default_color = "#000000"
        offset_x, offset_y = 0, 0

    else:
        img = Image.new("RGB", (img_w, img_h), hex_to_rgb(bg_color))
        draw = ImageDraw.Draw(img)
        offset_x, offset_y = 0, 0

    token_renkler = {}
    for token, token_style in style_obj:
        if token_style.get("color"):
            token_renkler[token] = "#" + token_style["color"]

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_boyutu)
    except:
        font = ImageFont.load_default()

    from pygments.lexers import get_lexer_by_name as glbn
    tokens = list(glbn(dil).get_tokens(kod))

    x = padding + satir_no_genislik + offset_x
    y = padding + offset_y
    satir_no = 1

    no_renk = (150, 130, 180) if stil != "⬜ Sade" else (150, 150, 150)
    cizgi_renk = (60, 40, 80) if stil != "⬜ Sade" else (200, 200, 200)

    draw.text((padding + offset_x, y), str(satir_no), font=font, fill=no_renk)
    draw.line([(padding + satir_no_genislik - 10 + offset_x, offset_y),
               (padding + satir_no_genislik - 10 + offset_x, img_h + offset_y)],
              fill=cizgi_renk, width=1)

    for ttype, value in tokens:
        renk = default_color
        if stil == "⬜ Sade":
            renk = "#000000"
        else:
            for parent in [ttype] + list(ttype.split()):
                if parent in token_renkler:
                    renk = token_renkler[parent]
                    break
        try:
            rgb = hex_to_rgb(renk)
        except:
            rgb = hex_to_rgb(default_color)

        parcalar = value.split("\n")
        for i, parca in enumerate(parcalar):
            if parca:
                draw.text((x, y), parca, font=font, fill=rgb)
                bbox = font.getbbox(parca)
                x += bbox[2] - bbox[0]
            if i < len(parcalar) - 1:
                x = padding + satir_no_genislik + offset_x
                y += char_h
                satir_no += 1
                draw.text((padding + offset_x, y), str(satir_no), font=font, fill=no_renk)

    return img


# ── Başlık ──
st.markdown('<div class="main-title">🌸 CodeSnap Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">── kod güzelleştirici ──</div>', unsafe_allow_html=True)

# ── GIF ──
if gif_base64:
    col_gif1, col_gif2, col_gif3 = st.columns([1, 2, 1])
    with col_gif2:
        st.markdown(gif_html, unsafe_allow_html=True)

st.divider()

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="section-header">🌸 Ayarlar</div>', unsafe_allow_html=True)

    dil = st.selectbox("Dil", ["python", "javascript", "java", "cpp", "html", "css"])
    tema = st.selectbox("Tema", ["nord", "dracula", "solarized-dark", "monokai", "github-dark"])
    png_stili = st.radio("PNG Stili", ["🎨 Temalı", "🌈 Degrade", "⬜ Sade"])
    font_boyutu = st.slider("Font Boyutu", 12, 24, 15)

    st.divider()

    st.markdown('<div class="section-header">🐙 GitHub\'dan Yükle</div>', unsafe_allow_html=True)
    repo_url = st.text_input("Repo URL", placeholder="https://github.com/kullanici/repo")

    if st.button("🔍 Dosyaları Listele"):
        if repo_url:
            try:
                with st.spinner("Repo taranıyor..."):
                    loader = GitHubLoader()
                    owner, repo_name, files = loader.get_files(repo_url)
                    st.session_state["github_owner"] = owner
                    st.session_state["github_repo"] = repo_name
                    st.session_state["github_files"] = files
                st.success(f"✅ {len(files)} dosya bulundu!")
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Lütfen repo URL girin!")

    if "github_files" in st.session_state:
        secilen_dosya = st.selectbox("Dosya Seç", st.session_state["github_files"])
        if st.button("📥 Dosyayı Yükle"):
            try:
                loader = GitHubLoader()
                content = loader.get_file_content(
                    st.session_state["github_owner"],
                    st.session_state["github_repo"],
                    secilen_dosya
                )
                st.session_state["kod"] = content
                st.success("✅ Yüklendi!")
            except ValueError as e:
                st.error(str(e))

# ── Ana alan ──
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">✏️ Kodunu Gir</div>', unsafe_allow_html=True)

    baslangic = st.session_state.get("kod", "# Kodunu buraya yaz\ndef merhaba():\n    print('Merhaba Dünya!')")
    kod = st.text_area("Kod", value=baslangic, height=400, label_visibility="collapsed")

    yuklenen = st.file_uploader("📂 Dosya Yükle", type=["py", "js", "java", "cpp", "html", "css"])
    if yuklenen:
        st.session_state["kod"] = yuklenen.read().decode("utf-8")
        st.rerun()

with col2:
    st.markdown('<div class="section-header">👁️ Önizleme & İndir</div>', unsafe_allow_html=True)

    if st.button("📸 Ekran Görüntüsü Al", type="primary", use_container_width=True):
        if not kod.strip():
            st.warning("Lütfen kod girin!")
        else:
            try:
                with st.spinner("🌸 PNG oluşturuluyor..."):
                    img = kod_to_png(kod, dil, tema, png_stili, font_boyutu)

                st.image(img, use_container_width=True)

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
                st.success("✅ Hazır!")

            except Exception as e:
                st.error(f"Hata: {str(e)}")