import discord
from discord.ext import commands
import json
import os
import random
import asyncio
import time

QUESTIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_questions(self):
        """Soruları JSON'dan okur."""
        if not os.path.exists(QUESTIONS_FILE):
            return []
        try:
            with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ [Quiz] questions.json bozuk.")
            return []

    @commands.command(name="quiz", aliases=["trivia"])
    async def quiz(self, ctx):
        """FRC Bilgi Yarışması! Rastgele bir FRC sorusu getirir.
        Kullanım: !quiz veya !trivia"""
        sorular = self.load_questions()

        if not sorular:
            return await ctx.send("❌ Veritabanında (questions.json) şu an hiç soru yok!")

        # Rastgele soru seçimi
        soru = random.choice(sorular)
        
        embed = discord.Embed(
            title="🧠 FRC Bilgi Yarışması!",
            description=f"**Soru:** {soru['question']}\n\n",
            color=discord.Color.gold()
        )
        
        # Şıkları ekleyelim
        for option in soru['options']:
            embed.description += f"▫️ {option}\n"
            
        bitis_zamani = int(time.time()) + 30
        
        embed.description += f"\n\nCevabını **A, B, C, veya D** olarak sohbete yaz!\n"
        embed.description += f"⏳ **Süren Bitiyor:** <t:{bitis_zamani}:R>"
        
        embed.add_field(name="📚 Kategori", value=soru.get("category", "Bilinmiyor"), inline=True)
        embed.add_field(name="⚖️ Zorluk", value=soru.get("difficulty", "Bilinmiyor"), inline=True)
        embed.set_footer(text="Oyundan çıkmak için sessizce beklemen yeterli.")

        await ctx.send(embed=embed)

        # Hangi kullanıcının cevabını kabul edeceğiz kontrolü (Sadece komutu girenden gelen ve aynı kanaldaki mesajı bekliyoruz)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            # Kullanıcıdan 30 saniye içinde mesaj bekle
            cevap_mesaji = await self.bot.wait_for('message', check=check, timeout=30.0)
            verilen_cevap = cevap_mesaji.content.strip().upper()
            dogru_cevap = soru['correct_answer'].upper()

            # Cevap kontrolü - A B C D gibi formatlara esneklik sağlayalım
            # Eğer kullanıcı 'A)' ya da 'A' yazdıysa ikisi de çalışsın
            gecerli_harfler = ['A', 'B', 'C', 'D']
            if len(verilen_cevap) >= 1 and verilen_cevap[0] in gecerli_harfler:
                alinan_harf = verilen_cevap[0]
                
                if alinan_harf == dogru_cevap:
                    await ctx.send(f"🎉 **Doğru Cevap!** Tebrikler {ctx.author.mention}, cevap gerçekten de **{dogru_cevap}** idi.")
                else:
                    await ctx.send(f"❌ **Yanlış Cevap.** Maalesef {ctx.author.mention}, doğru cevap **{dogru_cevap}** olacaktı.")
            else:
                 await ctx.send(f"⚠️ Geçersiz giriş yaptın {ctx.author.mention}. Lütfen sadece A, B, C veya D seç.")

        except asyncio.TimeoutError:
            # 30 saniye dolduğunda timeout düşer
            await ctx.send(f"⏳ Süren doldu {ctx.author.mention}! Doğru cevap **{soru['correct_answer']}** idi.")

async def setup(bot):
    await bot.add_cog(Quiz(bot))
