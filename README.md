# CodeSnap Pro

Kodu güzel PNG resimlerine dönüştüren masaüstü uygulaması.

---

## Gereksinimler

- Python 3.12
- wkhtmltoimage 0.12.6

---

## Kurulum

### 1. wkhtmltoimage Kur

https://wkhtmltopdf.org/downloads.html adresinden işletim sistemine uygun versiyonu indir ve kur.

**Windows için varsayılan kurulum yolu:**
```
C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe
```

> ⚠️ `screenshot.py` içindeki path'i kendi kurulum konumuna göre güncelle.

### 2. Sanal Ortam Oluştur

```bash
py -3.12 -m venv venv
```

### 3. Sanal Ortamı Aktif Et

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / Mac:**
```bash
source venv/bin/activate
```

### 4. Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Çalıştır

```bash
python main.py
```

---

## Kullanım

| Özellik | Nasıl Kullanılır |
|---|---|
| Kod yazma | Textbox'a direkt yaz |
| Dosya yükleme | "📂 dosya yükle" butonu |
| GitHub'dan yükleme | "🐙 github'dan yükle" butonu → repo URL gir |
| Tema seçimi | Üst paneldeki dropdown |
| Dil seçimi | Üst paneldeki dropdown |
| PNG stili | Temalı / Degrade / Sade radio button |
| Kayıt klasörü | "📁 kayıt klasörü seç" butonu |
| Ekran görüntüsü | "📸 ekran görüntüsü al" butonu |
| Uygulama teması | Ayarlar menüsü → Tema Değiştir |

---

## Desteklenen Diller

Python, JavaScript, Java, C++, HTML, CSS

## Desteklenen Kod Temaları

monokai, dracula, github

## Uygulama Temaları

Hacker, Okyanus, Gece, Arctic

---

## Proje Yapısı

```
CodeSnap Pro/
├── main.py               → Ana uygulama ve arayüz
├── highlighter.py        → Pygments kod renklendirici
├── screenshot.py         → HTML → PNG dönüştürücü
├── github_loader.py      → GitHub API entegrasyonu
├── syntax_highlighter.py → Gerçek zamanlı textbox renklendirici
├── theme_manager.py      → Tema yönetimi
├── requirements.txt      → Python bağımlılıkları
└── README.md             → Bu dosya
```
