import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from github_loader import GitHubLoader
import re

# ── Sayfa ayarları ──
st.set_page_config(
    page_title="CodeSnap Pro",
    page_icon="📸",
    layout="wide"
)

# ── Özel CSS ──
st.markdown("""
<style>
    /* Ana arka plan */
    .stApp {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a2e 50%, #0d0d0d 100%);
        animation: bgPulse 8s ease-in-out infinite;
    }

    @keyframes bgPulse {
        0%, 100% { background: linear-gradient(135deg, #0d0d0d 0%, #1a1a2e 50%, #0d0d0d 100%); }
        50% { background: linear-gradient(135deg, #0d0d0d 0%, #0d1a0d 50%, #0d0d0d 100%); }
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 20, 0.97);
        border-right: 1px solid #00ff4133;
        animation: sidebarGlow 3s ease-in-out infinite;
    }

    @keyframes sidebarGlow {
        0%, 100% { border-right-color: #00ff4122; }
        50% { border-right-color: #00ff4166; }
    }

    /* Typewriter başlık */
    .main-title {
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 3rem;
        font-weight: bold;
        color: #00ff41;
        text-shadow: 0 0 20px #00ff4166, 0 0 40px #00ff4133;
        overflow: hidden;
        white-space: nowrap;
        margin: 0 auto;
        animation: typewriter 2s steps(20, end), glowPulse 2s ease-in-out infinite 2s;
        width: fit-content;
    }

    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 20px #00ff4166, 0 0 40px #00ff4133; }
        50% { text-shadow: 0 0 30px #00ff41cc, 0 0 60px #00ff4166, 0 0 80px #00ff4133; }
    }

    /* Alt başlık fade-in */
    .sub-title {
        text-align: center;
        font-family: 'Courier New', monospace;
        color: #4a9e4a;
        font-size: 1rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in 2s both;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Butonlar */
    .stButton > button {
        background: linear-gradient(135deg, #143d14, #1a5e1a);
        color: #00ff41;
        border: 1px solid #00ff4144;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, #00ff4111, transparent);
        transform: rotate(45deg);
        transition: all 0.5s ease;
        opacity: 0;
    }

    .stButton > button:hover::before {
        animation: shimmer 0.5s ease forwards;
    }

    @keyframes shimmer {
        from { opacity: 0; left: -50%; }
        to { opacity: 1; left: 150%; }
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1a5e1a, #00ff41);
        color: #0d0d0d;
        border-color: #00ff41;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px #00ff4155, 0 0 40px #00ff4122;
    }

    /* Primary buton */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00ff41, #00cc33) !important;
        color: #0d0d0d !important;
        font-weight: bold !important;
        animation: primaryPulse 2s ease-in-out infinite;
    }

    @keyframes primaryPulse {
        0%, 100% { box-shadow: 0 0 10px #00ff4144; }
        50% { box-shadow: 0 0 25px #00ff4188, 0 0 50px #00ff4133; }
    }

    /* Text area */
    .stTextArea textarea {
        background: #111111 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff4133 !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        caret-color: #00ff41;
    }

    .stTextArea textarea:focus {
        border-color: #00ff41 !important;
        box-shadow: 0 0 15px #00ff4133 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #111111 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff4133 !important;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        border-color: #00ff41 !important;
        box-shadow: 0 0 10px #00ff4133;
    }

    /* Sidebar label */
    [data-testid="stSidebar"] label {
        color: #4a9e4a !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Bölüm başlıkları */
    .section-header {
        font-family: 'Courier New', monospace;
        color: #00ff41;
        font-size: 1.1rem;
        border-bottom: 1px solid #00ff4133;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-in;
    }

    /* Download butonu */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00ff41, #00cc33) !important;
        color: #0d0d0d !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
        animation: downloadPulse 1.5s ease-in-out infinite;
    }

    @keyframes downloadPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 10px #00ff4155; }
        50% { transform: scale(1.02); box-shadow: 0 0 25px #00ff4199; }
    }

    /* Resim fade-in */
    [data-testid="stImage"] {
        animation: imageFadeIn 0.8s ease-out;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 255, 65, 0.15);
    }

    @keyframes imageFadeIn {
        from { opacity: 0; transform: scale(0.95) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* Success mesajı */
    .stSuccess {
        animation: fadeIn 0.5s ease-in;
        border-left: 3px solid #00ff41 !important;
    }

    /* Error mesajı */
    .stError {
        animation: shake 0.5s ease-in-out;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #00ff41 !important;
    }

    /* Radio button */
    .stRadio label {
        color: #4a9e4a !important;
        font-family: 'Courier New', monospace !important;
        transition: color 0.3s ease;
    }

    .stRadio label:hover {
        color: #00ff41 !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] div {
        background: #00ff41 !important;
    }

    /* Divider */
    hr {
        border-color: #00ff4133 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0d0d;
    }
    ::-webkit-scrollbar-thumb {
        background: #00ff4166;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff41;
    }

    /* Matrix yağmur efekti arka planda */
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.03;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #00ff41;
        overflow: hidden;
    }
</style>

<canvas id="matrix" style="position:fixed;top:0;left:0;z-index:0;opacity:0.04;pointer-events:none;"></canvas>
<script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const chars = '01アイウエオカキクケコサシスセソ{}[]<>/\\|';
    const cols = Math.floor(canvas.width / 16);
    const drops = Array(cols).fill(1);
    function drawMatrix() {
        ctx.fillStyle = 'rgba(0,0,0,0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = '14px Courier New';
        drops.forEach((y, i) => {
            const char = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(char, i * 16, y * 16);
            if (y * 16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(drawMatrix, 50);
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c*2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def kod_to_png(kod, dil, tema, stil, font_boyutu=15):
    lexer = get_lexer_by_name(dil)
    formatter = HtmlFormatter(style=tema, noclasses=True)
    style_obj = get_style_by_name(tema)

    # Arka plan ve yazı rengini temadan al
    bg_color = style_obj.background_color or "#272822"
    default_color = "#f8f8f2"

    # HTML'den inline renkleri parse et
    renkli_html = highlight(kod, lexer, formatter)

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
        # Degrade arka plan
        img = Image.new("RGB", (img_w + 80, img_h + 80))
        draw = ImageDraw.Draw(img)
        for y in range(img_h + 80):
            oran = y / (img_h + 80)
            r = int(102 + (118 - 102) * oran)
            g = int(126 + (75 - 126) * oran)
            b = int(234 + (162 - 234) * oran)
            draw.line([(0, y), (img_w + 80, y)], fill=(r, g, b))

        # Kod kartı
        kart = Image.new("RGB", (img_w, img_h), hex_to_rgb(bg_color))
        img.paste(kart, (40, 40))
        draw = ImageDraw.Draw(img)
        offset_x = 40
        offset_y = 40

    elif stil == "⬜ Sade":
        img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        bg_color = "#ffffff"
        default_color = "#000000"
        offset_x = 0
        offset_y = 0

    else:  # Temalı
        img = Image.new("RGB", (img_w, img_h), hex_to_rgb(bg_color))
        draw = ImageDraw.Draw(img)
        offset_x = 0
        offset_y = 0

    # Pygments token renklerini al
    token_renkler = {}
    for token, stil_obj in style_obj:
        if stil_obj.get("color"):
            token_renkler[token] = "#" + stil_obj["color"]

    # Satırları çiz
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_boyutu)
        font_bold = ImageFont.truetype("DejaVuSansMono-Bold.ttf", font_boyutu)
    except:
        font = ImageFont.load_default()
        font_bold = font

    from pygments.token import Token
    from pygments.lexers import get_lexer_by_name as glbn

    lexer2 = glbn(dil)
    tokens = list(lexer2.get_tokens(kod))

    x = padding + satir_no_genislik + offset_x
    y = padding + offset_y
    satir_no = 1

    # Satır numarası çiz
    if stil == "⬜ Sade":
        no_renk = (150, 150, 150)
        cizgi_renk = (200, 200, 200)
    else:
        no_renk = (128, 128, 128)
        cizgi_renk = (60, 60, 60)

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
st.markdown('<div class="main-title">> CodeSnap Pro_</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">── kod güzelleştirici ──</div>', unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Ayarlar</div>', unsafe_allow_html=True)

    dil = st.selectbox("Dil", ["python", "javascript", "java", "cpp", "html", "css"])
    tema = st.selectbox("Tema", ["monokai", "dracula", "solarized-dark", "nord", "github-dark"])
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
                st.success(f"✅ Yüklendi!")
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
                with st.spinner("PNG oluşturuluyor..."):
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

            except Exception as e:
                st.error(f"Hata: {str(e)}")