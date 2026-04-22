import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler
load_dotenv()

# İzinleri (intents) ayarlıyoruz. Sadece default izinler ve message_content açık.
# Tüm yetkileri gereksiz yere açmıyoruz (örn: members, presences kapalı)
intents = discord.Intents.default()
intents.message_content = True  

# Bot nesnesini başlatıyoruz, prefix '!'
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Modüler komut ve event dosyalarını (cogs) yükleme fonksiyonu
async def load_extensions():
    # Güvenli bir şekilde commands ve events klasörlerini tarıyoruz
    klasorler = ['./commands', './events']
    
    for klasor in klasorler:
        if not os.path.exists(klasor):
            continue
            
        for filename in os.listdir(klasor):
            if filename.endswith('.py') and not filename.startswith('__'):
                cog_adi = f"{klasor[2:]}.{filename[:-3]}"
                try:
                    await bot.load_extension(cog_adi)
                    print(f"📦 Modül Yüklendi: {cog_adi}")
                except Exception as e:
                    print(f"❌ HATA: {cog_adi} modülü yüklenemedi! \nDetay: {e}")

# Bot başlatılırken eklentileri yüklemek için setup_hook kullanıyoruz
@bot.event
async def setup_hook():
    await load_extensions()

# Bot tamamen hazır olduğunda temiz bir log veriyoruz
@bot.event
async def on_ready():
    print("\n==============================================")
    print(f"✅ BAŞARILI: {bot.user.name} Discord'a bağlandı!")
    print(f"🆔 Bot ID  : {bot.user.id}")
    print(f"📡 Durum   : Çalışıyor ve Emir Bekliyor (!)")
    print("==============================================\n")

if __name__ == '__main__':
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if not TOKEN:
        print("❗ HATA: DISCORD_TOKEN bulunamadı!")
        print("Lütfen projenin ana dizininde bir '.env' dosyası oluşturduğunuzdan ve \nDISCORD_TOKEN=sizin_tokeniniz formatında girdiğinizden emin olun.")
    else:
        try:
            # Token geçerliyse botu başlat
            bot.run(TOKEN)
        except discord.errors.LoginFailure:
            print("❗ HATA: Girdiğiniz token geçersiz veya hatalı. Lütfen Developer Portal'dan token'ınızı teyit edin.")
        except Exception as e:
            print(f"❗ HATA: Beklenmedik bir sorun oluştu: {e}")
