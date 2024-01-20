from discord.ext import commands
from cogs.economy import Economy
import discord
import random
from asyncio import sleep

class Gambling(commands.Cog):
    eco = Economy()

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.eco.open()     

    @commands.command(pass_context=True)
    @commands.cooldown(1, 60*60*24, commands.BucketType.user)
    async def daily(self, ctx):
        """Her gün günlük paranızı alın!"""
        self.eco.add_money(ctx.author.id, 500)
        await ctx.send("Günlüğün olan 500₺ 'yi aldın.")

    @commands.command(pass_context=True)
    async def cash(self, ctx):
        """Elinizdeki para miktarını gösterir"""
        usr_money = self.eco.get_entry(ctx.author.id)[1]
        await ctx.send(f"Şu anda {usr_money}₺ paran var.")

    @commands.command(pass_context=True, aliases=['cf', 'coin'])
    async def coinflip(self, ctx, amount):
        """Biraz para kazanmak için yazı tura atın."""
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
        sonuc = random.randrange(1, 11)

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

    @commands.command(pass_context=True, aliases=['s', 'slot'])
    async def slots(self, ctx, miktar: int):
        """Paranla bahse girerek x10'e kadar kazan."""
        balance = self.eco.get_entry(ctx.author.id)[1]
        if miktar > balance:
            await ctx.send("Yeterli paran yok!")
            return
        emojis = ['apple', 'cherries', 'doughnut', 'grapes', 'taco', 'watermelon']

        await ctx.send(f"{ctx.author.name} {miktar}₺'sine bahse girdi.")

        slots = ['\t' for _ in range(3)]
        slot_spin = self.slot_spin(slots)

        slot_message = await ctx.send(slot_spin)

        for slot_num in range(3):
            for _ in range(4):
                slot = random.choice(emojis)
                slot = f':{slot}:'
                slots[slot_num] = slot
                slot_spin = self.slot_spin(slots)
                await slot_message.edit(content=slot_spin)
                await sleep(0.35)

        if slots[0] == slots[1] == slots[2]:
            miktar = miktar*10
            self.eco.add_money(ctx.author.id, miktar)
            out_text = f"{miktar}₺ kazandın! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        elif ( slots[0] == slots[1] or slots[0] == slots[2] or slots[1] == slots[2] ):
            miktar = miktar*2
            self.eco.add_money(ctx.author.id, miktar)
            out_text = f"{miktar}₺ kazandın! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        else:
            self.eco.remove_money(ctx.author.id, miktar)
            out_text = f"{miktar}₺ kaybettin! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        await ctx.send(out_text)

    def slot_spin(self, slots):
        return f'|\t{slots[0]}\t|\t{slots[1]}\t|\t{slots[2]}\t|'

        