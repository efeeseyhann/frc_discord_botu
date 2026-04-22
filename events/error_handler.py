import discord
from discord.ext import commands
import traceback
import sys

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Tüm komut bazlı hatalar bu fonksiyona düşer."""
        
        # Eğer bir komutun kendi özel hata fırlatıcısı varsa onu ezme, atla
        if hasattr(ctx.command, 'on_error'):
            return

        # Gerçek hatayı (çekirdek hatayı) çıkart
        error = getattr(error, 'original', error)

        # 1. Olmayan bir komut yazıldığında (Örn: !asdasdasd)
        if isinstance(error, commands.CommandNotFound):
            # Genelde her yanlış mesaja tepki vermemek için bu hata yutulur (sessiz kalınır)
            # Eğer görmek istersen alttaki '#' işaretini kaldır:
            # await ctx.send("⚠️ Kanka böyle bir komut bende yok, yanlış yazdın sanırım.")
            return

        # 2. Komuta zorunlu bir bilgi girilmediyse (MissingRequiredArgument)
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"⚠️ Eksik bilgi girdin. Lütfen komutu doğru kullandığından emin ol.\n(Hangi parametre eksik: `{error.param.name}`)")

        # 3. Bir üye bulunamadığında (MemberNotFound - Bizim !avatar komutunda olabilecek olan)
        if isinstance(error, commands.MemberNotFound):
            return await ctx.send("👤 Belirttiğin kişiyi sunucuda bulamadım. Doğru etiketleme (`@Kişi`) yaptığına emin ol.")
            
        # 4. Yetki eksikliği (MissingPermissions)
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("⛔ Kanka bu komutu kullanmak için yeterli yetkin bulunmuyor!")

        # 5. Bottan Dm'ye gönderilemeyen komutlar (NoPrivateMessage)
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send("Bu komut özel mesajlar üzerinden kullanılamaz.")
            except discord.HTTPException:
                pass

        # -------------------------------------------------------------
        # Yukarıdaki filtrelere takılmayan "Beklenmedik" gerçek hatalar
        # -------------------------------------------------------------
        
        # Kullanıcıya panik yaptırmayacak düzgün bir mesaj yolluyoruz
        await ctx.send("❌ Üzgünüm, bu komutu çalıştırırken beklenmedik bir sistem hatası oluştu.")
        
        # Geliştirici için terminale kırmızı orijinal traceback formunu yazdırıyoruz
        print("❗ Geliştirici Raporu: Beklenmeyen bir Command_Error oluştu!", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# main.py'nin bu eklentiyi otomatik yükleyebilmesi için gereklidir
async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
