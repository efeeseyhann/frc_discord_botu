import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Botun gecikmesini ms cinsinden gösterir."""
        gecikme = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Gecikme süresi: **{gecikme}ms**")

    @commands.command(name="merhaba")
    async def merhaba(self, ctx):
        """Kullanıcıyı etiketleyerek selam verir."""
        await ctx.send(f"Merhaba kanka, nasılsın? {ctx.author.mention} 👋")

    @commands.command(name="sunucu")
    async def sunucu(self, ctx):
        """Sunucu hakkında genel bilgileri bir embed içinde gösterir."""
        guild = ctx.guild
        
        # Eğer bu komut sunucu dışı özel mesajdan (DM) atılırsa onu engelliyoruz
        if guild is None:
            return await ctx.send("❗ Bu komut sadece sunucularda çalışır.")

        # Embed şablonu oluşturma
        embed = discord.Embed(
            title=f"📊 {guild.name} - Sunucu Bilgileri",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="🔑 Sunucu ID", value=guild.id, inline=True)
        embed.add_field(name="👥 Üye Sayısı", value=guild.member_count, inline=True)
        embed.add_field(name="💬 Kanal Sayısı", value=len(guild.channels), inline=True)
        
        # Sunucunun bir profil fotoğrafı (icon) varsa onu sağ üste ekliyoruz
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        await ctx.send(embed=embed)

    @commands.command(name="kullanici", aliases=["kullanıcı"])
    async def kullanici(self, ctx, uye: discord.Member = None):
        """Belirtilen kullanıcının veya komutu kullananın bilgilerini gösterir."""
        # Eğer bir kullanıcı etiketlenmemişse otomatik olarak mesajı yazan (ctx.author) alınsın
        uye = uye or ctx.author

        embed = discord.Embed(
            title="👤 Kullanıcı Bilgi Kartı",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Kullanıcı Adı", value=uye.name, inline=True)
        embed.add_field(name="Kullanıcı ID", value=uye.id, inline=True)
        
        # Tarih formatlamasını Gün/Ay/Yıl olacak şekilde düzeltiyoruz
        olusturma = uye.created_at.strftime("%d/%m/%Y")
        katilma = uye.joined_at.strftime("%d/%m/%Y") if uye.joined_at else "Bilinmiyor"
        
        embed.add_field(name="Hesap Oluşturma", value=olusturma, inline=False)
        embed.add_field(name="Sunucuya Katılım", value=katilma, inline=False)
        
        # Kullanıcının profil fotoğrafını alıyoruz, yoksa Discord'un varsayılan (gri vb) ikonunu alıyoruz
        if uye.avatar:
            embed.set_thumbnail(url=uye.avatar.url)
        else:
            embed.set_thumbnail(url=uye.default_avatar.url)

        await ctx.send(embed=embed)

# main.py dosyası eklentileri ararken bota bu cog'u tanıttığımız yer burasıdır
async def setup(bot):
    await bot.add_cog(General(bot))
