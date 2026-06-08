import requests  # internet üzerinden istek atmak için kullanıyoruz.API mantığı dışardan veri çekicez (indirmek gerekiyor pip)
# requests kütüphanesi Python'un yerleşik urllib'inden çok daha kolay kullanılır)(utllib hazır dır yani güncel olmaz)
# GitHub API'sine bağlanmak, dosya listesi çekmek, içerik almak için kullanacağız

import base64  # GitHub API dosya içeriğini base64 formatında gönderiyor
               # biz de onu çözüp normal metne çeviriyoruz  veriler karışmasın elmaya elma

class GitHubLoader:
    # Bu sınıfın tek görevi: GitHub'daki bir repo'ya bağlanıp
    # dosya listesini ve dosya içeriklerini çekmek.Kullanışlı olsun diye sadece tek dosya değil tüm ağacı istiyoruz

    def __init__(self, token=None):
        # GitHub API'sini token olmadan da kullanabilirsiniz,
        #ama bu sınırlı oluyor 60 istekmiş güncel olarak
        # token=None -> varsayılan olarak tokensiz başlıyoruz, (none yapmadan olmuyor )
        # ileride token eklemek istersek sadece buraya vermek yeterli. (Proje sadece oldu bitti değil gelişip büyümeye açık) :)
        self.__headers = {}
        if token:
            # Authorization(Yetki) header'ı GitHub'a "ben bu kullanıcıyım" demeyi sağlar.Güvenlik konturolü şart 
            # Header -> HTTP isteğinin üstbilgisi, kimlik ve ayar bilgilerini taşır.
            self.__headers["Authorization"] = f"token {token}"

    def get_files(self, repo_url):
        # Kullanıcının girdiği URL'den kullanıcı adı ve repo adını çıkarıyoruz.
        # Örnek: "https://github.com/kullanici/repo"
        # strip("/") -> sondaki / işaretini temizler
        # split("/") -> "/" ile böler -> ["https:", "", "github.com", "kullanici", "repo"]
        # parts[-2] -> sondan ikinci eleman -> "kullanici"
        # parts[-1] -> son eleman -> "repo" )Bu ikisini yapmamdaki sebep nokta atışı bulmak hata almamak
        parts = repo_url.strip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]

        # GitHub'ın "git trees" API'si repo'daki tüm dosyaları ağaç yapısında verir.
        # ?recursive=1 -> alt klasörlerin içindeki dosyaları da getir demek.
        # HEAD -> repo'nun en güncel halini getir demek.
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        response = requests.get(api_url, headers=self.__headers)

        # status_code -> sunucunun bize verdiği yanıt kodu
        # 200 ->başarılı, 404 -> bulunamadı, 403 -> erişim yasak gibi bunları internet üzerinden aldım hata kodları hakkına bilgim yok
        # 200 değilse bir sorun var demektir, kullanıcıya hata gösteriyoruz.
        if response.status_code != 200:
            raise ValueError(f"Repo bulunamadı veya erişim hatası: {response.status_code}")

        # response.json() -> gelen yanıtı Python sözlüğüne çevirir.Yoksa sadece düz metin olarak alır biz ayrısın sınıfa göre istiyotruz
        # "tree" anahtarı altında tüm dosya ve klasörler liste halinde gelir.
        data = response.json()

        # Sadece kod dosyalarını filtreliyoruz, görsel veya config dosyaları istemiyoruz.
        # item["type"] == "blob" -> blob dosya demek, tree ise klasör
        # item["path"].endswith(extensions) -> uzantısı listede olanları al çünkü farklı formatlar hataya sebep olur önüne geçmeliyiz
        # isintance kullanmak da olurdu aslında ama daha profesyonel olsun bi de bazı yerlerde hata alıyoruz
        extensions = (".py", ".js", ".java", ".cpp", ".html", ".css", ".ts")
        files = [item["path"] for item in data["tree"]
                 if item["type"] == "blob" and item["path"].endswith(extensions)]

        # owner ve repo'yu da döndürüyoruz çünkü
        # get_file_content metodunda bunlara tekrar ihtiyacımız olacak.
        return owner, repo, files

    def get_file_content(self, owner, repo, filepath):
        # GitHub'ın "contents" API'si belirli bir dosyanın içeriğini verir.
        # owner/repo/filepath -> hangi kullanıcı, hangi repo, hangi dosya
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
        response = requests.get(api_url, headers=self.__headers)

        if response.status_code != 200:
            raise ValueError(f"Dosya alınamadı: {response.status_code}")

        # GitHub API dosya içeriğini güvenli taşıma için base64 formatında gönderiyor.
        # base64 -> binary veriyi metin olarak taşımak için kullanılan bir kodlama sistemi.
        # b64decode ->base64'ü çözüp ham byte'a çevirir
        # .decode("utf-8") ->byte'ı normal Python string'ine çevirir
        # Türkçe karakterler için utf-8 şart, yoksa hata verir.Ki hata aldım ilk başlarda kabul etmedi ingilizce olmasına rağmen
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return content