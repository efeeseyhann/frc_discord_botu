import discord
from discord.ext import commands
import json
import os

HELP_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'help_topics.json')

class HelpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_topics(self):
        """JSON dosyasından yardım konularını okur."""
        if not os.path.exists(HELP_FILE):
            return {}
        try:
            with open(HELP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ [HelpSystem] help_topics.json okunurken bir hata oluştu.")
            return {}

    def normalize_input(self, text: str) -> str:
        """Kullanıcının Türkçe karakterli, büyük/küçük harfli girişini düzeltir."""
        if not text:
            return ""
        
        # Türkçe karakterleri İngilizce'ye çevirip sonrasında küçültüyoruz
        translation_table = str.maketrans("ıİşŞğĞüÜöÖçÇ", "iIsSgGuUoOcC")
        return text.translate(translation_table).lower().strip()

    @commands.command(name="helpme")
    async def helpme(self, ctx, *, category: str = None):
        """Yardım almak istediğin FRC kategorisine göre seni doğru kanallara yönlendirir.
        Kullanım: !helpme <kategori> (Örn: !helpme yazılım)"""
        topics = self.load_topics()

        # Konular hiç boş gelirse (ilk açılışta veya JSON hatalıysa) uyar
        if not topics:
            return await ctx.send("❌ Yardım konu veritabanı şu an boş veya okunamıyor.")

        # Kullanıcı kategori girmezse tüm mevcut kategorileri listele
        if category is None:
            mevcut_kategoriler = ", ".join([f"`{k}`" for k in topics.keys()])
            
            embed = discord.Embed(
                title="🛟 Hangi alanda desteğe ihtiyacın var?",
                description="Aşağıdaki konulardan biri hakkında yardım isteyebilirsin:\n\n"
                            f"{mevcut_kategoriler}\n\n"
                            "**Kullanım:** `!helpme <kategori adı>`",
                color=discord.Color.blue()
            )
            return await ctx.send(embed=embed)

        # Kullanıcının girdiği terimi (yazdır, YAZILIM vb) güvenli string formuna çevirip sözlükte bulalım
        safe_category = self.normalize_input(category)

        if safe_category not in topics:
            return await ctx.send(
                f"❌ Maalesef **'{category}'** isimli bir yardım alanımız yok.\n"
                f"Şu alanlardan birini dene: {', '.join([f'`{k}`' for k in topics.keys()])}"
            )

        # Konuyu bulduysak güzel bir yönlendirme kartı oluşturuyoruz
        istenen_konu = topics[safe_category]

        embed = discord.Embed(
            title=istenen_konu.get("title", "Yardım Desteği"),
            description=istenen_konu.get("description", "Bu kategori için açıklama girilmemiş."),
            color=discord.Color.brand_green()
        )

        kanallar = istenen_konu.get("suggested_channel", "Belirtilmemiş")
        roller = istenen_konu.get("suggested_role", "Belirtilmemiş")

        embed.add_field(name="💬 Sorman Gereken Kanal", value=kanallar, inline=False)
        embed.add_field(name="🙋 Etiketleyebileceğin Rol", value=roller, inline=False)
        embed.set_footer(text=f"Sorunu sorarken direkt hatayı/kodları da eklersen daha hızlı cevap alırsın!")
        embed.set_thumbnail(url=ctx.bot.user.display_avatar.url)  # Botun veya bir ünlem ikonunun resmi

        await ctx.send(content=f"Merhaba {ctx.author.mention}, işte sana yardımcı olacak bilgiler:", embed=embed)

async def setup(bot):
    await bot.add_cog(HelpSystem(bot))
