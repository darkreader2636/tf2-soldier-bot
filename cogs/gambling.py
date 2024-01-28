from discord.ext import commands
from cogs.economy import Economy
import discord
import random
from asyncio import sleep
import datetime

class Gambling(commands.Cog):
    eco = Economy()

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.eco.open()     

    @commands.command(pass_context=True)
    async def daily(self, ctx):
        """Her gün günlük paranızı alın!"""

        user_data = self.eco.get_entry(ctx.author.id)
        claim = user_data[4]
        curtime = int(datetime.datetime.now().timestamp())
        delta = curtime - claim
        cooldown = 60*60*20

        self.check_name(ctx.author.display_name, ctx.author.id)

        if delta < cooldown:
            await ctx.send(f"Bu günün parasını zaten aldın! Sonrakine kalan süre: <t:{claim + cooldown}:R>")
            return

        if delta > cooldown*2: #fark iki günden küçükse
            self.eco.set_streak(ctx.author.id, 0)
        else:
            self.eco.add_streak(ctx.author.id, 1)
            
        streak = self.eco.get_entry(ctx.author.id)[3]

        money_to_add = 500 + streak*10

        self.eco.add_money(ctx.author.id, money_to_add)
        self.eco.set_claim(ctx.author.id, curtime)
        await ctx.send(f"Günlüğün olan **{money_to_add}₺** 'yi aldın.\nSerin **{streak}** gün.")

    @commands.command(pass_context=True)
    async def cash(self, ctx):
        """Elinizdeki para miktarını gösterir"""
        self.check_name(ctx.author.display_name, ctx.author.id)
        usr_money = self.eco.get_entry(ctx.author.id)[1]
        await ctx.send(f"Şu anda {usr_money}₺ paran var.")

    @commands.command(pass_context=True, aliases=['cf', 'coin'])
    async def coinflip(self, ctx, amount):
        """Biraz para kazanmak için yazı tura atın."""
        self.check_name(ctx.author.display_name, ctx.author.id)
        if amount == "all":
            if balance < 2500:
                amount = balance
            else:
                amount = 2500
        else:
            amount = int(amount)

        if amount < 0:
            await ctx.send("Miktar sıfırdan küçük olamaz!")
            return
        balance = self.eco.get_entry(ctx.author.id)[1]
    
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
        """Birbirinize para gönderin!"""
        self.check_name(ctx.author.display_name, ctx.author.id)
        balance = self.eco.get_entry(ctx.author.id)[1]
        if amount > balance:
            await ctx.send("Yeterli paran yok!")
            return
        self.eco.remove_money(ctx.author.id, amount)
        self.eco.add_money(hedef.id, amount)
        await ctx.send(f"<@{ctx.author.id}> <@{hedef.id}>'ye {amount}₺ gönderdi.")

    @commands.command(pass_context=True, aliases=['s', 'slot'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def slots(self, ctx, amount):
        """Paranla bahse girerek x10'e kadar kazan."""
        self.check_name(ctx.author.display_name, ctx.author.id)
        balance = self.eco.get_entry(ctx.author.id)[1]

        if amount == "all":                                                                                                              
            if balance < 2500:                                                                                                            
                amount = balance                                                                                                          
            else:                                                                                                                      
                amount = 2500                                                                                                             
        else:                                                                                                                             
            amount = int(amount)

        if amount < 0:
            await ctx.send("Miktar sıfırdan küçük olamaz!")
            return
        
        if amount > balance:
            await ctx.send("Yeterli paran yok!")
            return
        emojis = ['flag_cm', 'flag_et', 'flag_mm', 'flag_sn', 'flag_vn', 'flag_gh']

        await ctx.send(f"{ctx.author.name} {amount}₺'sine bahse girdi.")

        await ctx.send("**`___SLOTS___`**")

        slots = [':black_large_square:' for _ in range(3)]
        slot_spin = self.slot_spin(slots)

        slot_message = await ctx.send(slot_spin)

        await ctx.send("`|         |`")

        for slot_num in range(3):
            for _ in range(4):
                slot = random.choice(emojis)
                slot = f':{slot}:'
                slots[slot_num] = slot
                slot_spin = self.slot_spin(slots)
                await slot_message.edit(content=slot_spin)
                await sleep(0.35)

        if slots[0] == slots[1] == slots[2]:
            amount = amount*10
            self.eco.add_money(ctx.author.id, amount)
            out_text = f"{amount}₺ kazandın! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        elif ( slots[0] == slots[1] or slots[0] == slots[2] or slots[1] == slots[2] ):
            amount = amount*2
            self.eco.add_money(ctx.author.id, amount)
            out_text = f"{amount}₺ kazandın! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        else:
            self.eco.remove_money(ctx.author.id, amount)
            out_text = f"{amount}₺ kaybettin! Paran: {self.eco.get_entry(ctx.author.id)[1]}₺"

        await ctx.send(out_text)

    @commands.command(pass_context=True, aliases=['t'])
    async def top(self, ctx,):
        """En zengin 10 Kişiyi görün"""
        message_to_send = "En Zengin 10 kişi:\n"
        for user in enumerate(self.eco.top_entries(10)):
            id = user[0]+1
            user= user[1]
            name = user[2]
            money = user[1]
            str_to_append = f"{id}) {name} {money}₺\n"
            message_to_send = message_to_send+str_to_append
        message_to_send = message_to_send + "`(Eğer isminiz düzgün değilse .tf2 cash ile düzeltebilirsiniz)`"
        await ctx.send(message_to_send)

    def slot_spin(self, slots):
        return f'` `{slots[0]}{slots[1]}{slots[2]}` ` .'
    
    def check_name(self, name: str, user_id: int):
        user_name = self.eco.get_entry(user_id)[2]
        if(user_name == name):
            return
        self.eco.set_name(user_id, name)
        return
        
