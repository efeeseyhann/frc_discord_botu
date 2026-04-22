import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["pp", "profil"])
    async def avatar(self, ctx, uye: discord.Member = None):
        """Kullanıcının veya belirtilen kişinin profil fotoğrafını büyütülmüş olarak gösterir."""
        # Eğer kişi etiketlenmediyse, komutu kullanan kişiyi hedef al
        uye = uye or ctx.author
        
        embed = discord.Embed(
            title=f"🖼️ {uye.name} Profil Fotoğrafı",
            color=discord.Color.purple()
        )
        
        # Kullanıcının kendi avatarı yoksa varsayılan discord avatarını al
        if uye.avatar:
            embed.set_image(url=uye.avatar.url)
        else:
            embed.set_image(url=uye.default_avatar.url)
            
        await ctx.send(embed=embed)

    @commands.command(name="roll", aliases=["dice"])
    async def roll(self, ctx):
        """1 ile 6 arasında rastgele bir sayı atar."""
        sonuc = random.randint(1, 6)
        await ctx.send(f"🎲 Zarı attın ve... **{sonuc}** geldi!")

    @commands.command(name="coinflip", aliases=["flip"])
    async def coinflip(self, ctx):
        """Havaya bir bozuk para atar (Yazı / Tura)."""
        secenekler = ["Yazı", "Tura"]
        sonuc = random.choice(secenekler)
        await ctx.send(f"🪙 Parayı havaya attın ve... **{sonuc}!**")

# main.py'nin bu komutları tanıması için gereken kurulum fonksiyonu
async def setup(bot):
    await bot.add_cog(Fun(bot))
