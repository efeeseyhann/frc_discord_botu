from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="zar")
    async def zar(self, ctx):
        """1 ile 6 arasında rastgele bir zar atar."""
        sonuc = random.randint(1, 6)
        await ctx.send(f'🎲 Zarı attın ve **{sonuc}** geldi!')

async def setup(bot):
    await bot.add_cog(Fun(bot))
