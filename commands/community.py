import discord
from discord.ext import commands
import random
from utils.team_database import (
    add_team, get_team, search_teams_by_name,
    search_teams_by_country, get_all_teams, get_team_count
)


class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ----------------------------------------------------------------
    # !registerteam
    # ----------------------------------------------------------------
    @commands.command(name="registerteam")
    @commands.guild_only()
    async def registerteam(self, ctx, team_number: int = None, *, rest: str = None):
        """Global FRC veritabanına yeni bir takım kaydeder.
        Kullanım: !registerteam <numara> <takım_adı> <ülke> <şehir> <rookie/veteran>"""

        # Parametre kontrolü
        if team_number is None or rest is None:
            embed = discord.Embed(
                title="❌ Eksik Bilgi",
                description="Takım eklemek için tüm bilgileri girin.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Doğru Kullanım:",
                value="`!registerteam <numara> <takım_adı> <ülke> <şehir> <rookie/veteran>`\n"
                      "Örnek: `!registerteam 10998 Voltaria Robotics Turkey Aksaray rookie`",
                inline=False
            )
            return await ctx.send(embed=embed)

        words = rest.split()

        if len(words) < 4:
            return await ctx.send(
                "❌ Yetersiz bilgi! En az **takım adı**, **ülke**, **şehir** ve **rookie/veteran** gerekiyor.\n"
                "Örnek: `!registerteam 10998 Voltaria Robotics Turkey Aksaray rookie`"
            )

        rookie_or_veteran = words[-1]
        city = words[-2]
        country = words[-3]
        team_name = " ".join(words[:-3])

        if rookie_or_veteran.lower() not in ("rookie", "veteran"):
            return await ctx.send("❌ Son kelime sadece **rookie** veya **veteran** olabilir!")

        success = add_team(
            team_number=team_number,
            team_name=team_name,
            country=country,
            city=city,
            rookie_or_veteran=rookie_or_veteran.capitalize(),
            registered_by_user_id=ctx.author.id
        )

        if not success:
            return await ctx.send(f"⚠️ **{team_number}** numaralı takım zaten veritabanında kayıtlı!")

        embed = discord.Embed(
            title="✅ Takım Başarıyla Kaydedildi!",
            color=discord.Color.green()
        )
        embed.add_field(name="🔢 Numara", value=str(team_number), inline=True)
        embed.add_field(name="🤖 İsim", value=team_name, inline=True)
        embed.add_field(name="🌍 Ülke", value=country, inline=True)
        embed.add_field(name="🏙️ Şehir", value=city, inline=True)
        embed.add_field(name="🏅 Deneyim", value=rookie_or_veteran.capitalize(), inline=True)
        embed.set_footer(text=f"Kaydeden: {ctx.author.name} • Toplam: {get_team_count()} takım")

        await ctx.send(embed=embed)

    @registerteam.error
    async def registerteam_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Takım numarası sadece rakamlardan oluşmalıdır!\n"
                           "Örnek: `!registerteam 10998 Voltaria Robotics Turkey Aksaray rookie`")

    # ----------------------------------------------------------------
    # !teamprofile
    # ----------------------------------------------------------------
    @commands.command(name="teamprofile")
    @commands.guild_only()
    async def teamprofile(self, ctx, team_number: int = None):
        """Takım numarasıyla global veritabanından takım kartını gösterir."""
        if team_number is None:
            return await ctx.send("❌ Takım numarası girin. Örnek: `!teamprofile 10998`")

        team = get_team(team_number)
        if not team:
            return await ctx.send(f"⚠️ **{team_number}** numaralı takım veritabanında bulunamadı.")

        embed = discord.Embed(
            title=f"🤖 FRC #{team['team_number']} — {team['team_name']}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔢 Takım No", value=str(team["team_number"]), inline=True)
        embed.add_field(name="🌍 Ülke", value=team["country"], inline=True)
        embed.add_field(name="🏙️ Şehir", value=team["city"], inline=True)
        embed.add_field(name="🏅 Deneyim", value=team["rookie_or_veteran"], inline=True)

        if team.get("description"):
            embed.add_field(name="📝 Açıklama", value=team["description"], inline=False)

        embed.set_footer(text=f"Kayıt: {team.get('created_at', '?')[:10]} • Kaydeden ID: {team.get('registered_by_user_id', '?')}")

        await ctx.send(embed=embed)

    @teamprofile.error
    async def teamprofile_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Takım numarası sadece rakamlardan oluşmalıdır! Örnek: `!teamprofile 10998`")

    # ----------------------------------------------------------------
    # !teamsearch
    # ----------------------------------------------------------------
    @commands.command(name="teamsearch")
    @commands.guild_only()
    async def teamsearch(self, ctx, *, keyword: str = None):
        """İsim veya numaraya göre takım arar."""
        if keyword is None:
            return await ctx.send("❌ Aranacak bir kelime veya numara girin. Örnek: `!teamsearch Voltaria`")

        results = []

        if keyword.isdigit():
            team = get_team(int(keyword))
            if team:
                results.append(team)

        name_results = search_teams_by_name(keyword)
        for t in name_results:
            if t not in results:
                results.append(t)

        if not results:
            return await ctx.send(f'⚠️ **"{keyword}"** ile eşleşen bir takım bulunamadı.')

        embed = discord.Embed(
            title=f'🔍 "{keyword}" Arama Sonuçları',
            description=f"{len(results)} takım bulundu:",
            color=discord.Color.purple()
        )

        for team in results[:10]:
            embed.add_field(
                name=f"#{team['team_number']} — {team['team_name']}",
                value=f"📍 {team['city']}, {team['country']} • {team['rookie_or_veteran']}",
                inline=False
            )

        if len(results) > 10:
            embed.set_footer(text=f"...ve {len(results) - 10} takım daha.")

        await ctx.send(embed=embed)

    # ----------------------------------------------------------------
    # !discoverteam / !randomteam
    # ----------------------------------------------------------------
    @commands.command(name="discoverteam", aliases=["randomteam"])
    @commands.guild_only()
    async def discoverteam(self, ctx):
        """Veritabanından rastgele bir FRC takımı getirir. Keşfetmeye başla!"""
        all_teams = get_all_teams()

        if not all_teams:
            return await ctx.send("⚠️ Veritabanında henüz kayıtlı takım yok. İlk takımı `!registerteam` ile sen ekle!")

        team = random.choice(all_teams)

        embed = discord.Embed(
            title="🎲 Rastgele FRC Takımı Keşfi",
            description="Veritabanından senin için bir takım seçtim!",
            color=discord.Color.magenta()
        )
        embed.add_field(name="🤖 Takım", value=f"**#{team['team_number']}** — {team['team_name']}", inline=False)
        embed.add_field(name="🌍 Ülke", value=team["country"], inline=True)
        embed.add_field(name="🏙️ Şehir", value=team["city"], inline=True)
        embed.add_field(name="🏅 Deneyim", value=team["rookie_or_veteran"], inline=True)

        if team.get("description"):
            embed.add_field(name="📝 Açıklama", value=team["description"], inline=False)

        embed.set_footer(text=f"Toplam {len(all_teams)} takım arasından seçildi • Tekrar denemek için !discoverteam yaz")

        await ctx.send(embed=embed)

    # ----------------------------------------------------------------
    # !discovercountry
    # ----------------------------------------------------------------
    @commands.command(name="discovercountry")
    @commands.guild_only()
    async def discovercountry(self, ctx, *, country: str = None):
        """Belirtilen ülkedeki tüm FRC takımlarını listeler."""
        if country is None:
            return await ctx.send("❌ Ülke adı girin. Örnek: `!discovercountry Turkey`")

        results = search_teams_by_country(country)

        if not results:
            return await ctx.send(f"⚠️ **{country}** ülkesinde kayıtlı takım bulunamadı.")

        embed = discord.Embed(
            title=f"🌍 {country.title()} — FRC Takımları",
            description=f"Bu ülkede **{len(results)}** kayıtlı takım bulundu:",
            color=discord.Color.dark_teal()
        )

        for team in results[:15]:
            embed.add_field(
                name=f"#{team['team_number']} — {team['team_name']}",
                value=f"📍 {team['city']} • {team['rookie_or_veteran']}",
                inline=False
            )

        if len(results) > 15:
            embed.set_footer(text=f"...ve {len(results) - 15} takım daha.")
        else:
            embed.set_footer(text="Başka ülkeleri de keşfetmek için !discovercountry <ülke> yazın!")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Community(bot))
