# pygments kütüphanesinden sadece ihtiyacımız olan parçaları çekiyoruz.
# Tüm kütüphaneyi import etmek yerine "from,import "kullanıyoruz.Çünkü karışıklığı azaltmak için from mesela i.inden almak için kullanılır
# çünkü gereksiz her şeyi belleğe yüklemek istemiyoruz.
from pygments import highlight #şef
from pygments.lexers import get_lexer_by_name  # dile göre çözümleyici getirir. Altın kelimeleri buluyoruz gibi
from pygments.formatters import HtmlFormatter   # renklendirmeyi HTML formatına çevirir adı üstünde

# Kodun ne anlama geldiğini anlayan (lexer) ve onu renkli HTML'e çeviren (formatter)
# bu üç araç birlikte çalışır:
# get_lexer_by_name -> "bu Python kodu, şu kelime anahtar, şu fonksiyon" gibi ayırır
# HtmlFormatter ->ayrılan parçaları seçilen temaya göre renklendirir
#  highlight -> ikisini birleştirip bize HTML çıktısı verir )şef mantığı)

class CodeHighlighter:
    # Bu sınıf tek bir iş yapıyor: kodu alıp renkli HTML'e çevirmek.
    # Dışarıdan kod, tema ve dil bilgisi alıyor, içeride bunları saklıyor.

    def __init__(self, code, theme="monokai", language="python"):
        # Çift alt çizgi (__) ile başlayan değişkenler "private" yani gizlidir.(BU hatırlatma unutma hata kodları burdan kaynaklı hep)
        # Dışarıdan doğrudan erişilemez, sadece bu sınıfın kendi metodları kullanabilir.
        # Bunu yapıyoruz çünkü veriyi korumak istiyoruz — kimse gelip kodu
        # ya da temayı kontrol mekanizmasını atlayarak değiştiremesin.(şerrefsiz kullanıcılar için önlem)!!!!
        self.__code = code
        self.__theme = theme
        self.__language = language

    # Property decorator'ı bir metodu "özellik gibi" kullanmamızı sağlar.
    # highlighter.code() demek yerine highlighter.code diyebiliyoruz.(Büyük bir artı aslında hem kolaylık hemde karmaşıklığın önüne geçiyoruz)
    # Bu sayede dışarıdan okuma yapılabilir ama doğrudan yazma yapılamaz.
    @property
    def code(self):
        return self.__code

    @property
    def language(self):
        return self.__language

    @property
    def theme(self):
        return self.__theme

    @theme.setter
    def theme(self, new_theme):
        # Setter, bir property'ye değer atanmak istendiğinde devreye girer.
        # Yani highlighter.theme = "dracula" yapıldığında burası çalışır.
        # Böylece geçersiz tema atanmasını engelliyoruz — doğrulama burada olur.
        supported_themes = ["monokai", "dracula", "github"]

        # Gelen tema desteklenen listede varsa güvenle atıyoruz.
        # "in" operatörü listedeki elemanları teker teker kontrol eder.(içinde var mı yok mu)
        if new_theme in supported_themes:
            self.__theme = new_theme
        else:
            # Geçersiz tema gelirse ValueError fırlatıyoruz.
            # Bu hatayı main.py'daki try-except bloğu yakalayacak
            # ve kullanıcıya mesaj gösterecek.
            raise ValueError(f"Yanlış seçim: '{new_theme}' desteklenen bir tema değil.")

    def highlight_code(self):
        # Dil bilgisine göre doğru lexer'ı getiriyoruz.
        # Artık sadece Python değil, JavaScript, Java, C++ vb. de destekleniyor.(dil hakimiyeti kısmı yapay zeka ile yapıldı)
        # get_lexer_by_name("python") -> Python lexer'ı getirir
        # get_lexer_by_name("javascript") -> JS lexer'ı getirir
        lexer = get_lexer_by_name(self.__language)

        # Seçilen temaya göre HTML formatter oluşturuyoruz.
        # style parametresi pygments'in hazır temalarından birini kullanır.
        formatter = HtmlFormatter(style=self.theme, noclasses=True)

        # highlight fonksiyonu üç şeyi bir araya getirir:
        # kodu + lexer (anlayan) + formatter (renkleyen) -> renkli HTML çıktısı
        return highlight(self.code, lexer, formatter)
    def get_css(self):
        # Temanın arka plan rengini de içeren CSS'i döndürür
        formatter = HtmlFormatter(style=self.theme, noclasses=True)
        return formatter.get_style_defs('body')