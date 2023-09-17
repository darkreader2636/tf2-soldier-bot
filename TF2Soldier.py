# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import os
import http.client
import json
from discord.ext import tasks
import asyncio
from dotenv import load_dotenv
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''TF2 Soldier. Discord.py kullanılarak yapılan basit bir bot. Bir sıkıntı olursa @darkreader2636 ile iletişime geçin'''

bot = commands.Bot(command_prefix='.tf2 ', description=description, intents=intents)

load_dotenv()

with open('karaliste.txt', 'r') as f:
    words = f.read()
    badwords = words.splitlines()

#static vars
response = {
  "gmod": "<@1008352427885465691> <@998201530639470642> <@831138134669918238> gmod girek."
}

img_response = {
  "buneamk": "./bunemm.jpg",
  "kahkaha": "./kahkaha.gif",
  "alperinbacusu": "./onay.jpg"
}

memes = os.listdir("./memes/")
shitposts = os.listdir("./shitpost/")
stopper = 0

def namazvakit():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 4tgdakJZiRJ8NBGPXpEdQ0:1zRXT1cRU9OZYBUQJnplrg"
        }

    conn.request("GET", "/pray/all?data.city=kastamonu", headers=headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        return json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents, ensure_ascii=False)
    else:
        return json.dumps(json_thing, sort_keys=sort, indent=indents)
    return None

@bot.event
async def on_ready():
    global stopper
    stopper = 0
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('--------------------------------------------')
    print(datetime.datetime.now())
    kalan_gun.start()

@tasks.loop(minutes=1)
async def kalan_gun():
    if (datetime.datetime.now().hour == 14 and datetime.datetime.now().minute == 30):
        today = datetime.date.today()
        future = datetime.date(2024, 1, 22)
        diff = future - today
        channel = bot.get_channel(1150499657437417492)
        print("sent")
        await channel.send('Yarıyıl Tatiline {0} gün kaldı.'.format(str(diff)[:3]))


@bot.command()
async def add(ctx, left: int, right: int):
    """İki sayıyı toplar. (add <sayı> <sayı>)"""
    await ctx.send(left + right)


@bot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))
 
@bot.command()
async def hızlı(ctx, rp: str ):
    """   Hızlı yanıt modu. (hızlı <mesaj>)"""
    await ctx.send(response[rp])

@bot.command()
async def meme(ctx):
    """Rastgele bir resim gönderir."""
    selected_file = random.choice(memes)
    path = os.path.join("./memes", selected_file)
    print("Sending: ", path)
    await ctx.send(file=discord.File(path))

@bot.command()
async def alper(ctx, istek: str):
    if ( ctx.guild.id == 1122457879660724265):
        """Alperin söylediği efsane şarkıları yollar. (pepe, kısa, uzun)""",
        mp3file = "./alper_{}.mp3".format(istek)
        print("Sending: ", mp3file)
        await ctx.send(file=discord.File(mp3file))
    else:
        await ctx.send("Bilinmeyen Komut")

@bot.command()
async def repeat(ctx, times: int, *, content='repeating...'):
    """Bir mesajı tekrarlar. (repeat <miktar> <mesaj>)"""
    global stopper
    if stopper:
        stopper = False
    if times > 200:
        await ctx.send("200'den fazla repeat gönderemezsin")
        return
    for i in range(times):
        if stopper:
            print("STOP")
            break
        await ctx.send(content)
    return
    
@bot.command()
async def namaz(ctx):
    """Namaz vakitlerini gösterir."""
    await ctx.send(pp_json(namazvakit()))

@bot.command()
async def dur(ctx):
    """Repeat komutunu durdurur."""
    global stopper
    stopper = True

@bot.command()
async def resim(ctx, *, resim):
    """İsmi verilen resmi gönderir"""
    print("Sending: {}".format(resim))
    if ctx.message.reference is not None:
        ctx = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    await ctx.reply(file=discord.File(img_response[resim]), mention_author=False)
    
@bot.command()
async def shitpost(ctx):
    """Rastgele bir shitpost gönderir."""
    selected_sp = random.choice(shitposts)
    patsp = os.path.join("./shitpost", selected_sp)
    print("Sending: Shitpost ", patsp)
    await ctx.send(file=discord.File(patsp))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Bilinmeyen komut: {0}".format(ctx.message.content))

bot.run(os.getenv('TOKEN'))
