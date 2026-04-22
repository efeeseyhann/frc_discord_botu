import discord
from discord.ext import commands
from utils.user_profile_database import (
    get_or_create_profile, get_profile, update_profile_field,
    get_user_count, VALID_ROLES
)
from utils.team_database import get_team


class UserProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------
    # !introduce <bio>
    # ----------------------------------------------------------------
    @commands.command(name="introduce")
    async def introduce(self, ctx, *, bio: str = None):
        """Kendini toplulukta tanıt. Biyografi yazarsan herkese görünür olur.
        Kullanım: !introduce <kısa tanıtım yazısı>"""

        if bio is None:
            return await ctx.send(
                "✏️ Lütfen bir tanıtım yazısı ekle!\n"
                "Örnek: `!introduce Merhaba! Türkiye'de FRC oynayan bir yazılım üyesiyim.`"
            )

        if len(bio) > 200:
            return await ctx.send("❌ Tanıtım yazısı en fazla **200 karakter** olabilir.")

        profile = update_profile_field(
            user_id=ctx.author.id,
            display_name=ctx.author.display_name,
            short_bio=bio
        )

        embed = discord.Embed(
            title="✅ Profilin Güncellendi!",
            description=f"Tanıtım yazın kaydedildi.",
            color=discord.Color.green()
        )
        embed.add_field(name="📝 Biyografi", value=bio, inline=False)
        embed.set_footer(text=f"Profil bilgilerini tamamlamak için !setrole ve !setcountry komutlarını da dene.")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    # ----------------------------------------------------------------
    # !profile [@kullanıcı]
    # ----------------------------------------------------------------
    @commands.command(name="profile")
    async def profile(self, ctx, uye: discord.Member = None):
        """Kendi veya belirtilen kişinin FRC profilini gösterir.
        Kullanım: !profile veya !profile @kişi"""

        uye = uye or ctx.author
        profile = get_profile(uye.id)

        if profile is None:
            if uye == ctx.author:
                return await ctx.send(
                    "⚠️ Henüz bir profilin yok!\n"
                    "`!introduce <tanıtım yazısı>` komutuyla profil oluşturabilirsin."
                )
            else:
                return await ctx.send(f"⚠️ **{uye.display_name}** henüz bir profil oluşturmamış.")

        embed = discord.Embed(
            title=f"👤 {profile['display_name']} — FRC Profili",
            color=discord.Color.blurple()
        )

        # Rol alanı
        rol = profile.get("role_area")
        embed.add_field(
            name="⚙️ Rol Alanı",
            value=rol.capitalize() if rol else "Belirtilmemiş",
            inline=True
        )

        # Ülke
        ulke = profile.get("country")
        embed.add_field(
            name="🌍 Ülke",
            value=ulke if ulke else "Belirtilmemiş",
            inline=True
        )

        # Takım numarası — varsa global veritabanından adını da çek
        takim_no = profile.get("team_number")
        if takim_no:
            takim = get_team(takim_no)
            takim_deger = f"#{takim_no} — {takim['team_name']}" if takim else f"#{takim_no}"
        else:
            takim_deger = "Belirtilmemiş"
        embed.add_field(name="🤖 Takım", value=takim_deger, inline=True)

        # Biyografi
        bio = profile.get("short_bio")
        if bio:
            embed.add_field(name="📝 Hakkında", value=bio, inline=False)

        # Kayıt tarihi
        kayit = profile.get("created_at", "")[:10]
        embed.set_footer(text=f"Profil oluşturuldu: {kayit}")
        embed.set_thumbnail(url=uye.display_avatar.url)

        await ctx.send(embed=embed)

    # ----------------------------------------------------------------
    # !setrole <rol>
    # ----------------------------------------------------------------
    @commands.command(name="setrole")
    async def setrole(self, ctx, *, rol: str = None):
        """FRC'deki rol alanını belirler.
        Geçerli roller: software, mechanical, electrical, pr, mentor, student, other"""

        gecerli_roller = ", ".join(f"`{r}`" for r in VALID_ROLES)

        if rol is None:
            return await ctx.send(
                f"❌ Rol adı girilmedi!\n"
                f"Geçerli roller: {gecerli_roller}\n"
                f"Örnek: `!setrole software`"
            )

        rol_lower = rol.lower().strip()

        if rol_lower not in VALID_ROLES:
            return await ctx.send(
                f"❌ **'{rol}'** geçerli bir rol değil.\n"
                f"Geçerli roller: {gecerli_roller}"
            )

        update_profile_field(
            user_id=ctx.author.id,
            display_name=ctx.author.display_name,
            role_area=rol_lower
        )

        await ctx.send(f"✅ Rol alanın **{rol_lower.capitalize()}** olarak güncellendi!")

    # ----------------------------------------------------------------
    # !setcountry <ülke>
    # ----------------------------------------------------------------
    @commands.command(name="setcountry")
    async def setcountry(self, ctx, *, ulke: str = None):
        """Profilindeki ülke bilgisini günceller.
        Kullanım: !setcountry Turkey"""

        if ulke is None:
            return await ctx.send("❌ Ülke adı girilmedi! Örnek: `!setcountry Turkey`")

        if len(ulke) > 60:
            return await ctx.send("❌ Ülke adı çok uzun!")

        update_profile_field(
            user_id=ctx.author.id,
            display_name=ctx.author.display_name,
            country=ulke.strip()
        )

        await ctx.send(f"✅ Ülke bilgin **{ulke.strip()}** olarak güncellendi!")

    # ----------------------------------------------------------------
    # !setteamnumber <numara>
    # ----------------------------------------------------------------
    @commands.command(name="setteamnumber")
    async def setteamnumber(self, ctx, team_number: int = None):
        """Profilini global takım veritabanındaki takıma bağlar.
        Kullanım: !setteamnumber 10998"""

        if team_number is None:
            return await ctx.send("❌ Takım numarası girilmedi! Örnek: `!setteamnumber 10998`")

        # Takım global veritabanında kayıtlı mı kontrol et
        takim = get_team(team_number)
        if not takim:
            return await ctx.send(
                f"⚠️ **{team_number}** numaralı takım global veritabanında bulunamadı.\n"
                f"Önce `!registerteam` komutuyla takımı eklemen gerekiyor."
            )

        update_profile_field(
            user_id=ctx.author.id,
            display_name=ctx.author.display_name,
            team_number=team_number
        )

        await ctx.send(f"✅ Takımın **#{team_number} — {takim['team_name']}** olarak güncellendi!")

    @setteamnumber.error
    async def setteamnumber_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Takım numarası sadece rakamlardan oluşmalıdır! Örnek: `!setteamnumber 10998`")


async def setup(bot):
    await bot.add_cog(UserProfile(bot))
