import discord
from discord.ext import commands
from utils.guild_config import set_guild_config, get_guild_config, is_setup_complete

class FRCCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setupteam")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def setupteam(self, ctx, team_number: int = None, *, team_name: str = None):
        """Bu sunucu için FRC takım numarasını ve adını ayarlar."""

        # 2. Parametre Eksikliği Kontrolü
        if team_number is None or team_name is None:
            embed = discord.Embed(
                title="❌ Eksik veya Hatalı Kullanım",
                description="Takım numarasını ve adını girmelisiniz.",
                color=discord.Color.red()
            )
            embed.add_field(name="Doğru Kullanım:", value="`!setupteam <takım_numarası> <takım_adı>`\nÖrnek: `!setupteam 10998 Voltaria Robotics`")
            return await ctx.send(embed=embed)

        # 3. Veriyi JSON'a Kaydetme
        try:
            # set_guild_config fonksiyonu otomatik olarak setup_completed değerini true yapacaktır
            set_guild_config(ctx.guild.id, team_name, team_number)
            
            # Başarı mesajı (Sade ve şık Embed)
            embed = discord.Embed(
                title="✅ FRC Takım Kurulumu Başarılı",
                description="Sunucunuz için takım bilgileri başarıyla kaydedildi.",
                color=discord.Color.green()
            )
            embed.add_field(name="Takım Numarası", value=str(team_number), inline=True)
            embed.add_field(name="Takım Adı", value=team_name, inline=True)
            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=f"Kurulumu yapan: {ctx.author.name}")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send("❌ Veriler kaydedilirken beklenmeyen bir hata oluştu. Lütfen geliştiriciye bildirin.")
            print(f"HATA (setupteam): {e}")

    # Özel hata yakalayıcı (Hatalı yazımlar ve Yetki yoksunluğu için)
    @setupteam.error
    async def setupteam_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("⛔ **Erişim Reddedildi:** Bu komutu kullanabilmek için 'Sunucuyu Yönet' (Manage Server) veya Yöneticilik yetkilerine sahip olmanız gerekmektedir.")
        elif isinstance(error, commands.BadArgument):
            # team_number için rakam yerine yazı girildiğinde bu hata fırlar (örn: !setupteam Voltaria 10998)
            await ctx.send("❌ **Geçersiz Takım Numarası:** Takım numarası sadece rakamlardan oluşmalıdır!\nÖrnek kural: `!setupteam 10998 Voltaria Robotics`")

    @commands.command(name="teaminfo")
    @commands.guild_only()
    async def teaminfo(self, ctx):
        """Bu sunucuya ait kayıtlı FRC takım bilgilerini gösterir."""

        if not is_setup_complete(ctx.guild.id):
            return await ctx.send("⚠️ **Bilgi Yok:** Bu sunucuda henüz bir FRC takımı yapılandırılmamış. Lütfen yetkililerden `!setupteam` komutunu kullanmalarını isteyin.")

        config = get_guild_config(ctx.guild.id)
        team_name = config.get("team_name", "Bilinmiyor")
        team_number = config.get("team_number", "Bilinmiyor")
        
        embed = discord.Embed(
            title="⚙️ FRC Takım Bilgileri",
            color=discord.Color.gold()
        )
        embed.add_field(name="📌 Sunucu Adı", value=ctx.guild.name, inline=False)
        embed.add_field(name="🤖 Takım Adı", value=team_name, inline=True)
        embed.add_field(name="🔢 Takım Numarası", value=str(team_number), inline=True)
        embed.add_field(name="✅ Kurulum", value="Tamamlanmış", inline=True)
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
            
        await ctx.send(embed=embed)

    @commands.command(name="teamstatus")
    @commands.guild_only()
    async def teamstatus(self, ctx):
        """Botun FRC modülasyonunun bu sunucudaki durumunu kontrol eder."""

        setup_ok = is_setup_complete(ctx.guild.id)
        
        embed = discord.Embed(
            title="📡 FRC Modül Durumu",
            description="Sunucunuz için özel FRC entegrasyonu durumu aşağıdadır:",
            color=discord.Color.green() if setup_ok else discord.Color.orange()
        )
        
        if setup_ok:
            embed.add_field(name="Modül Aktifliği", value="✅ Çalışıyor", inline=False)
            embed.add_field(name="Kurulum", value="✅ Veritabanına kayıt bağlandı.", inline=False)
            embed.set_footer(text="Takım bilgilerini görmek için !teaminfo yazabilirsiniz.")
        else:
            embed.add_field(name="Modül Aktifliği", value="⏸️ Beklemede", inline=False)
            embed.add_field(name="Kurulum Tutarsızlığı", value="❌ Bu sunucuda bir takım tanıtılmamış.", inline=False)
            embed.add_field(name="Nasıl Çözülür?", value="Lütfen bir yönetici çağırarak `!setupteam <numara> <isim>` kurulumunu yapın.", inline=False)
            
        await ctx.send(embed=embed)

# main.py bağlayıcısı
async def setup(bot):
    await bot.add_cog(FRCCog(bot))
