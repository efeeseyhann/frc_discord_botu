from discord.ext import commands

class ReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Bot başarıyla giriş yaptığında çalışır."""
        print(f'{self.bot.user.name} olarak giriş yapıldı!')
        print(f'Bot ID: {self.bot.user.id}')
        print('------')

async def setup(bot):
    await bot.add_cog(ReadyEvent(bot))
