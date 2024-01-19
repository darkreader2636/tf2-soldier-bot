from discord.ext import commands
from economy import Economy
import discord
import random

class Gambling(commands.Cog):
    eco = Economy()

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.eco.open()     

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        self.eco.add_money(ctx.author.id, 500)
        await ctx.send("Günlüğün olan 500₺ 'yi aldın.")

    @commands.command(pass_context=True)
    async def cash(self, ctx):
        usr_money = self.eco.get_entry(ctx.author.id)[1]
        await ctx.send(f"Şu anda {usr_money}₺ paran var.")

    @commands.command(pass_context=True)
    async def cf(self, ctx, amount):
        balance = self.eco.get_entry(ctx.author.id)[1]
        if amount == "all":
            if balance < 2500:
                amount = balance
            else:
                amount = 2500
        else:
            amount = int(amount)
    
        if amount > balance:
            await ctx.send("Yeterli paran yok!")
            return
        sonuc = random.randrange(0,11)

        if sonuc < 5:
            self.eco.remove_money(ctx.author.id, amount)
            usr_money = self.eco.get_entry(ctx.author.id)[1]
            await ctx.send(f"{amount}₺ kaybettin! Paran:{usr_money}₺")

        else:
            self.eco.add_money(ctx.author.id, amount)
            usr_money = self.eco.get_entry(ctx.author.id)[1]
            await ctx.send(f"{amount}₺ kazandın! Paran:{usr_money}₺")
    
    @commands.command(pass_context=True)
    async def send(self, ctx, hedef: discord.User, amount: int):

        balance = self.eco.get_entry(ctx.author.id)[1]
        if amount > balance:
            await ctx.send("Yeterli paran yok!")
            return
        self.eco.remove_money(ctx.author.id, amount)
        self.eco.add_money(hedef.id, amount)
        await ctx.send(f"<@{ctx.author.id}> <@{hedef.id}>'ye {amount}₺ gönderdi.")

        