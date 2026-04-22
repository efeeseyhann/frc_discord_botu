# 🤖 Discord Bot Projesi

## 📖 Projenin Amacı
Bu proje, tamamen modüler ve yönetimi kolay bir alt yapıya sahip, prefix (`!`) tabanlı bir Discord bot iskeletidir. Yeni başlayanların karmaşık yapılar içinde kaybolmadan kendi komutlarını ekleyip büyütebilecekleri, gelişmiş hata yönetimi yapabilen temiz bir temel sistem sunar.

## 💻 Kullanılan Teknolojiler
- **Python (3.8+)**: Botun yazılarak çalıştırıldığı ana yazılım dili.
- **discord.py**: Discord ile kodumuzun iletişim kurmasını sağlayan resmi API kütüphanesi.
- **python-dotenv**: Güvenlik ve token (şifre) yönetimi için ortam değişkenlerini okuyan kütüphane.

## 📂 Proje Yapısı
```text
FRC_dc_bot/
├── main.py              # Botun ana merkez (motor) dosyası. Tüm komutları ve olayları buradan çalıştırır.
├── .env                 # (Sizin üreteceğiniz) Botun şifresinin bulunduğu gizli dosya.
├── .env.example         # .env dosyasını nasıl oluşturacağınızı gösteren örnek şablon.
├── requirements.txt     # Botun ihtiyaç duyduğu dış kütüphanelerin listesi.
├── commands/            # Botun verdiği tepkilerin ve komutların bulunduğu klasör.
│   ├── general.py       # Ping, sunucu bilgi gibi genel komutlar.
│   └── fun.py           # Avatar, zar atma gibi eğlence komutları.
├── events/              # Botun arka planda dinlediği veya gözlemlediği olaylar (-events-).
│   ├── ready.py         # Bot açıldığında terminale bilgi geçme olayı.
│   └── error_handler.py # Hatalı bir kod yazıldığında programın çökmesini veya sohbeti kirletmesini engelleyen koruma modülü.
└── utils/               # Proje genelinde kullanılabilecek ortak fonksiyonlar bulundurur.
```

## 🛠️ Adım Adım Kurulum

### 1. Python Sürüm Kontrolü
Botun sağlıklı çalışabilmesi için bilgisayarında en az Python 3.8 yüklü olmalıdır. İşletim sisteminin arama kısmına `cmd` yazıp komut istemini açın ve şunu yazın:
```bash
python --version
```

### 2. Sanal Ortam (Virtual Environment) Oluşturma
Projenizin ihtiyaç duyduğu kütüphanelerin tüm bilgisayarınızı kirletmemesi için proje klasöründe izole bir sanal alan (`.venv`) oluşturmalıyız:
```bash
python -m venv .venv
```

### 3. Sanal Ortamı Aktif Etme
Her şeyden önce bu izole klasörün kapısını açmalıyız, yoksa sistem komutlarımızı görmez.
- **Windows için:**
  ```bash
  .\.venv\Scripts\activate
  ```
- **Mac/Linux için:**
  ```bash
  source .venv/bin/activate
  ```
*(Klasörü başarıyla aktif ettiğinizde komut satırının en solunda parantez içinde `(.venv)` yazısını görmelisiniz.)*

### 4. Gerekli Kütüphaneleri Kurma
Sanal ortam çalışıyorken, arka planda eksik olan `discord.py` ve eklentilerini kuruyoruz:
```bash
pip install -r requirements.txt
```

### 5. .env Dosyası Hazırlama
Projenin ana dizininde (klasöründe) `.env` isimli (başında sadece nokta olan) yeni bir dosya oluşturun. İçerisine tıpkı örnekteki gibi şunu yazın:
```env
DISCORD_TOKEN=SENIN_URUN_TOKENIN_BURAYA_YAPISTIRILACAK
```
**⚠️ GÜVENLİK NOTU:** Bu dosyada bulunan Token, botunuzun kimlik numarası ve kumandasıdır. Bu şifreyi **asla** başkalarıyla paylaşmamalı ve Github gibi açık yerlere yüklememelisiniz!

---

## 🔑 Token Alma ve Botu Ayarlama

### 1. Discord Developer Portal'dan Token Alma
1. [Discord Developer Portal](https://discord.com/developers/applications) adresine gidin.
2. Sağ üstten **New Application** diyerek botunuza bir ad verin.
3. Soldaki menüden **Bot** sekmesine geçin.
4. Çıkan ekranda **Reset Token** butonuna basın. Size karışık harflerden oluşan uzun bir metin (Token) verecektir.
5. Bu dizini kopyalayıp, oluşturduğunuz `.env` dosyasının içindeki eşittir (=) işaretinden sonraya yapıştırın.

### 2. Message Content Intent Açma (ÇOK ÖNEMLİ)
Biz botumuzda Slash Command (/) değil, **Prefix Command (!)** sistemini kullandık. Discord'un yeni kuralları gereği mesaj okumak izne tabidir; bu yüzden botun insanların `!ping` yazdığını görebilmesi için alttaki ayarı açmak zorundasınız:
1. Developer Portal üzerinden **Bot** sekmesini biraz aşağıya kaydırın.
2. **Privileged Gateway Intents** başlığı bulunuyor.
3. Oradaki üç şalterden **Message Content Intent** şalterini MAVİ (Açık) konuma getirip alttaki yeşil Save (Kaydet) tuşuna basın.

### 3. Botu Sunucuya Ekleme
1. Sol taraftaki menüde yer alan **OAuth2 -> URL Generator** sekmesine dokunun.
2. Ana penceredeki `SCOPES` kısmından SADECE `bot` seçeneğini işaretleyin.
3. Altta yeni bir pencere açılacak. Oradaki `BOT PERMISSIONS` (Bot İzinleri) listesinden `Administrator` (Yönetici) seçeneğini seçin.
4. Sayfanın en alt kısmında yeşil bir link oluşacak. Bu linki kopyalayıp yeni bir tarayıcı sekmesine yapıştırırsanız, botu kendi sunucularınıza ekleyebilirsiniz.

---

## 🚀 Botu Çalıştırma
Tüm adımları başarıyla geçtiyseniz, sanal ortamınızın (`.venv`) aktif olduğundan emin olun ve terminalinize giderek start komutunu verin:
```bash
python main.py
```
Alt kısımlarda `✅ BAŞARILI: Botunuz Discord'a bağlandı!` cümlesinden oluşan yeşil renkli terminal penceresini gördüğünüz an, her şey hazır demektir.

---

## 📜 Mevcut Komut Listesi
Botun şu andaki aktif çalıştırıcı ön eki **`!`** sembolüdür. Hazır gelen komutlar şu şekildedir:

**Genel Komutlar:**
- `!ping` : Botun aktif hızını ve tepkime süresini (ms) döndürür.
- `!merhaba` : Komutu çağıran üyeye etiket atarak selam verir.
- `!sunucu` : Sunucunun mevcut istatistiklerini temiz bir tablo/embed içinde verir.
- `!kullanici` veya `!kullanıcı [@kişi]` : Sizin ya da etiketlenen argümanın, kuruluş ve katılış gibi ana bilgilerini listeler.

**Eğlence Komutları:**
- `!avatar` veya `!avatar [@kişi]` : Profil fotoğrafını büyütülmüş olarak kaliteli çözünürlükte sohbet penceresine yansıtır.
- `!zar` : Bota izole bir zar attırır (1-6).
- `!yazitura` : Belirlenmiş olasılıklar üzerinden rastgele madeni para attırır.

---

## ❓ Yaygın Hatalar ve Olası Çözümleri

- **Hata Tipi:** `ModuleNotFoundError: No module named 'dotenv'` veya `No module named 'discord'`
  **Olası Çözüm:** Sanal ortamı (`.venv`) başarıyla aktif edememişsiniz veya requirements.txt içinde bulunan dosyaları kurmamışsınız demektir. Kurulumdaki Adım 3 ve 4 alanını titizlikle tekrar edin.

- **Hata Tipi:** `❗ HATA: DISCORD_TOKEN bulunamadı!`
  **Olası Çözüm:** `.env` dosyanızı ya yanlış bir konuma (bir klasörün içine) açtınız ya da dosya adını kaydederken Windows görünmeyen yerlerde `.env.txt` gibi bir isimle kaydetti. Adı kesinlikle çıplak halde `.env` olmalıdır.

- **Hata Tipi:** Bot aktif olarak ayağa kalkıyor ancak yazılan `!ping` komutunun hiçbirine cevap vermiyor.
  **Olası Çözüm:** Developer Portal sitesi üzerinden **Message Content Intent** (Mesaj Okuma İzni) ayarını aktif etmeyi unuttunuz. Orayı açın, kaydedin ve botun komut satırına gelip `CTRL + C` tuş kombinasyonuyla botu durdurup tekrar `python main.py` yazarak başlatın.

> Not: Discord Botum hala test aşamasında gelişlemer oldukça buraya push edeceğim.
