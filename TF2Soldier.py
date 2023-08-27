# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import os
import http.client
import json
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''TF2 Soldier. Discord.py kullanılarak yapılan basit bir bot. Bir sıkıntı olursa @darkreader2636 ile iletişime geçin'''

bot = commands.Bot(command_prefix='.tf2 ', description=description, intents=intents)

#static vars
response = {
  "gmod": "<@1008352427885465691> <@998201530639470642> <@831138134669918238> gmod girek."
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
    stopper_task.start()

@tasks.loop(seconds=1)  # task runs every 60 seconds
async def stopper_task():
    global stopper
    stopper = False

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
    """Alperin söylediği efsane şarkıları yollar. (pepe, kısa, uzun)"""
    mp3file = "./alper_{}.mp3".format(istek)
    print("Sending: ", mp3file)
    await ctx.send(file=discord.File(mp3file))

@bot.command()
async def repeat(ctx, times: int, *, content='repeating...'):
    """Bir mesajı tekrarlar. (repeat <miktar> <mesaj>)"""
    global stopper
    if times > 200:
        await ctx.send("200'den fazla repeat gönderemezsin")
        return
    for i in range(times):
        if not stopper:
            await ctx.send(content)
        break
    
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
async def buneamk(ctx):
    print("Sending: Bune")
    await ctx.send(file=discord.File("./bunemm.jpg"))
    
@bot.command()
async def alperinbacusu(ctx):
    print("Sending: onay.jpg")
    await ctx.send(file=discord.File("./onay.jpg"))
    
@bot.command()
async def shitpost(ctx):
    """Rastgele bir shitpost gönderir."""
    selected_sp = random.choice(shitposts)
    patsp = os.path.join("./shitpost", selected_sp)
    print("Sending: Shitpost ", patsp)
    await ctx.send(file=discord.File(patsp))

bot.run('MTEzODE5NTA4NjI3NDk5ODMxMg.GsEk4L.VgyHh5T33tR7YVK9ePpFMClETANYeZheGmiHbI')
