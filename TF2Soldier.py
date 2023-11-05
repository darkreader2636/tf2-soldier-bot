# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import os
from discord.ext import tasks
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import datetime
from deep_translator import GoogleTranslator
import pickle
import asyncio


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''TF2 Soldier. Discord.py kullanılarak yapılan basit bir bot. Bir sıkıntı olursa @darkreader2636 ile iletişime geçin'''

bot = commands.Bot(command_prefix='.tf2 ', description=description, intents=intents)

load_dotenv()

#static vars

global response
with open('response.pkl', 'rb') as f:
    response = pickle.load(f)

global badwords
with open('karaliste.txt', 'r') as f:
    words = f.read()
    badwords = words.splitlines()

img_response = {
  "buneamk": "./images/bunemm.jpg",
  "buneamk 2": "./images/buneamk2.jpg",
  "kahkaha": "./images/kahkaha.gif",
  "alperinbacusu": "./images/onay.jpg",
  "salih": "./images/salih.mp4",
  "ney": "./images/ney.jpg",
  "al oc": "./images/parmak.mp4"
}

memes = os.listdir("./memes/")
shitposts = os.listdir("./shitpost/")
hl_shitposts = os.listdir("./hl1/")
stopper = 0

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def namazgonder():
    r = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/9609/kastamonu-icin-namaz-vakti")
    source = BeautifulSoup(r.content,"lxml")
    tarih = source.find("div",attrs={"class":"ti-hicri"})
    tarih = tarih.text
    tarih = tarih.replace("\n","")
    imsak = source.find("div",attrs={"data-vakit-name":"imsak"}).find("div",attrs={"class":"tpt-time"}).text
    imsak = "İmsak Vakti : "+imsak+"\n"
    gunes = source.find("div",attrs={"data-vakit-name":"gunes"}).find("div",attrs={"class":"tpt-time"}).text
    gunes = "Güneş Vakti : "+gunes+"\n"
    oglen = source.find("div",attrs={"data-vakit-name":"ogle"}).find("div",attrs={"class":"tpt-time"}).text
    oglen = "Öğlen Vakti : "+oglen+"\n"
    ikindi = source.find("div",attrs={"data-vakit-name":"ikindi"}).find("div",attrs={"class":"tpt-time"}).text
    ikindi = "İkindi Vakti : "+ikindi+"\n"
    aksam = source.find("div",attrs={"data-vakit-name":"aksam"}).find("div",attrs={"class":"tpt-time"}).text
    aksam = "Akşam Vakti : "+aksam+"\n"
    yatsi = source.find("div",attrs={"data-vakit-name":"yatsi"}).find("div",attrs={"class":"tpt-time"}).text
    yatsi = "Yatsı Vakti : "+yatsi+"\n"
    vakit = imsak+gunes+oglen+ikindi+aksam+yatsi
    return vakit

@bot.event
async def on_ready():
    global stopper
    stopper = 0
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('--------------------------------------------')
    print(datetime.datetime.now())
    kalan_gun.start()
    await bot.tree.sync()

@bot.event
async def on_message(message: discord.Message):
    channel = bot.get_channel(1156596803291058227)
    if message.author == bot.user:
        return
    if message.guild is None and not message.author.bot:
        await channel.send(message.content)
    if contains_word(message.content.lower(), "sa") and not  message.author.bot:
        await message.channel.send("as")
    if contains_word(message.content.lower(), "ney") and not  message.author.bot:
        await message.channel.send(file=discord.File(img_response["ney"]))
    await kufur_kontrol(message, message.author)
    await bot.process_commands(message)

async def kufur_kontrol(message, user):
    global badwords
    msg = message.content.lower()
    user = message.author
    for word in badwords:
        if word in msg:
            if contains_word(msg, word):
                channel = bot.get_channel(1169648813414305833)
                embed=discord.Embed(title="Küfür Kaydı", color=0xff0000)
                embed.add_field(name="Kullanıcı", value = message.author, inline=True)
                embed.add_field(name="Kanal", value = message.channel, inline=True)
                embed.add_field(name="Mesaj", value = message.content, inline=False)
                embed.add_field(name="Yasaklı Kelime", value = word, inline=True)
                embed.add_field(name="Tarih", value=str(datetime.datetime.now()), inline=True)
                await channel.send(embed=embed)
                dm_embed = discord.Embed(title="Küfür Kaydı", color=0xff0000)
                dm_embed.add_field(name="Sunucu", value = message.guild, inline=True)
                dm_embed.add_field(name="Kanal", value = message.channel, inline=True)
                dm_embed.add_field(name="Mesaj", value = message.content, inline=False)
                dm_embed.add_field(name="Yasaklı Kelime", value = word, inline=True)
                dm_embed.add_field(name="Tarih", value=str(datetime.datetime.now()), inline=True)
                await user.send(embed=dm_embed)
                await asyncio.sleep(0.5)
                await message.delete()
                break
    return

@tasks.loop(minutes=1)
async def kalan_gun():
    if (datetime.datetime.now().hour == 14 and datetime.datetime.now().minute == 30):
        today = datetime.date.today()
        future = datetime.date(2024, 1, 22)
        diff = future - today
        channel = bot.get_channel(1150499657437417492)
        print("sent")
        await channel.send('Yarıyıl Tatiline {0} gün kaldı.'.format(str(diff)[:3]))


@bot.hybrid_command()
async def add(ctx, left: int, right: int):
    """İki sayıyı toplar. (add <sayı> <sayı>)"""
    await ctx.send(left + right)

@bot.hybrid_command()
async def çevir(ctx, istek: str, hedef: str):
    translated = GoogleTranslator(source='auto', target=hedef).translate(text=istek)  
    await ctx.send(translated)


@bot.hybrid_command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.hybrid_command()
async def karaliste_ekle(ctx, kelime: str):
    global badwords
    with open('karaliste.txt', 'a') as f:
        f.write("{0}\n".format(kelime))
    with open('karaliste.txt', 'r') as f:
        words = f.read()
        badwords = words.splitlines()
    await ctx.send("Eklendi!")
 
@bot.hybrid_command()
async def hızlı(ctx, rp: str ):
    """   Hızlı yanıt modu. (hızlı <mesaj>)"""
    await ctx.send(response[rp])

@bot.hybrid_command()
async def hızlı_ekle(ctx, name: str , tmp: str):
    global response
    if name not in response.keys():
        response[name] = tmp
    with open('response.pkl', 'wb') as f:
        pickle.dump(response, f)
    with open('response.pkl', 'rb') as f:
        response = pickle.load(f)

@bot.hybrid_command()
async def meme(ctx):
    """Rastgele bir resim gönderir."""
    selected_file = random.choice(memes)
    path = os.path.join("./memes", selected_file)
    print("Sending: ", path)
    await ctx.send(file=discord.File(path))

@bot.hybrid_command()
async def alper(ctx, istek: str):
    if ( ctx.guild.id == 1122457879660724265):
        """Alperin söylediği efsane şarkıları yollar. (pepe, kısa, uzun)""",
        mp3file = "./alper_{}.mp3".format(istek)
        print("Sending: ", mp3file)
        await ctx.send(file=discord.File(mp3file))
    else:
        await ctx.send("Bilinmeyen Komut")

@bot.hybrid_command()
async def repeat(ctx, times: int, *, content):
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
    
@bot.hybrid_command()
async def namaz(ctx):
    """Namaz vakitlerini gösterir."""
    await ctx.send(namazgonder())

@bot.hybrid_command()
async def dur(ctx):
    """Repeat komutunu durdurur."""
    global stopper
    stopper = True

@bot.hybrid_command()
async def resim(ctx, *, resim):
    """İsmi verilen resmi gönderir"""
    print("Sending: {}".format(resim))
    if ctx.message.reference is not None:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        await message.reply("<@{0}> tarafından gönderildi.".format(ctx.author.id),file=discord.File(img_response[resim]), mention_author=False)
        await ctx.message.delete()
    else:
        message = ctx
        await message.send("<@{0}> tarafından gönderildi.".format(ctx.author.id),file=discord.File(img_response[resim]), mention_author=False)
    await ctx.message.delete()
    
    
@bot.hybrid_command()
async def shitpost(ctx):
    """Rastgele bir shitpost gönderir."""
    selected_sp = random.choice(shitposts)
    patsp = os.path.join("./shitpost", selected_sp)
    print("Sending: Shitpost ", patsp)
    await ctx.send(file=discord.File(patsp))

@bot.hybrid_command()
async def hl_shitpost(ctx):
    """Rastgele bir Half-Life shitpostu gönderir."""
    selected_hl = random.choice(hl_shitposts)
    pathl = os.path.join("./hl1", selected_hl)
    print("Sending: HL Shitpost ", pathl)
    await ctx.send(file=discord.File(pathl))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Bilinmeyen komut: {0}".format(ctx.message.content))

bot.run(os.getenv('TOKEN'))
