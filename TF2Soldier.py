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
from time import perf_counter 
from logger import my_logger


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''TF2 Soldier. Discord.py kullanılarak yapılan basit bir bot. Bir sıkıntı olursa @darkreader2636 ile iletişime geçin'''

bot = commands.Bot(command_prefix='.tf2 ', description=description, intents=intents)
log = my_logger()

load_dotenv()

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
  "al oc": "./images/parmak.mp4",
  "gabe": "./images/gabe.png",
  "bi durun": "./images/bidurun.jpg",
  "kek": "./images/kek.jpg",
  "trombon": "./images/trombon.mp4",
  "ets2": "./images/ets2.png",
  "hl3": "./images/hl3.png",
  "metro": "./images/metro.png"
}

memes = os.listdir("./memes/")
shitposts = os.listdir("./shitpost/")
hl_shitposts = os.listdir("./hl1/")
stopper = 0

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def namazgonder():
    timer_start = perf_counter()
    r = requests.get("https://namazvakitleri.diyanet.gov.tr/tr-TR/9609/kastamonu-icin-namaz-vakti",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
    log.INFO(f"Got 1 page in {perf_counter() - timer_start} seconds.")
    source = BeautifulSoup(r.content,"html.parser")
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

def fiyatlar():
    t1_start = perf_counter()

    main_page = BeautifulSoup(requests.get("https://www.bloomberght.com/").content,"html.parser")

    usd     = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'USDTRY Curncy'}).get_text()
    eur     = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'EURTRY Curncy'}).get_text()
    gbp     = main_page.find('tr', class_='tab-content-bottom-list live-ingiliz-sterlini').find_next('td', class_='LastPrice').text
    ceyrek  = main_page.find('tr', class_='tab-content-bottom-list live-gram-altin').find_next('td', class_='LastPrice').text
    bist    = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'XU100 Index'}).get_text()
    faiz    = main_page.find('small', class_='value LastPrice', attrs={'data-secid':'TAHVIL2Y'}).get_text()

    log.INFO(f"Got 1 page in {perf_counter() - t1_start} seconds.")

    #final= "USD/TRY: {0}\nEUR/TRY: {1}\nGBP/TRY: {2}\nÇeyrek Satış: {3}\nBIST 100: {4}\nFaiz: {5}".format(usd,eur,gbp,ceyrek,bist,faiz)
    embed = discord.Embed(title="Döviz Kurları", color=0xff0000, description="Son Güncelleme: <t:{0}:t>".format(int(datetime.datetime.now().timestamp())))
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/d/d7/Philippine-stock-market-board.jpg")
    embed.add_field(name="Dolar/TL:", value = usd, inline=True)
    embed.add_field(name="Euro/TL:", value = eur, inline=True)
    embed.add_field(name="Sterlin/TL:", value = gbp, inline=True)
    embed.add_field(name="Çeyrek Alış:", value = ceyrek, inline=True)
    embed.add_field(name="BIST 100:", value = bist, inline=True)
    embed.add_field(name="Faiz:", value = faiz, inline=True)
    return embed

def benzin_fiyat():
    t1_start = perf_counter()
    r = requests.get("https://www.petrolofisi.com.tr/akaryakit-fiyatlari",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'})
    log.INFO(f"Got 1 page in {perf_counter() - t1_start} seconds.")

    sec = BeautifulSoup(r.content,"html.parser").findAll('li')

    for item in sec:
        if "KASTAMONU" in item.text:
            result = item
            break
        else: 
            pass

    new_soup = BeautifulSoup(result.prettify(),"html.parser")
    for i in new_soup.findAll('div', class_='mt-2'): #Remove child element of <div>'s
        i.find_next().decompose()

    out = new_soup.findAll('div', class_='mt-2')

    list = []
    for tip in out:
        list.append(tip.get_text().strip())
    embed=discord.Embed(title="Akaryakıt Fiyatları", 
    url="https://www.petrolofisi.com.tr/akaryakit-fiyatlari", 
    description="Son Güncelleme: <t:{0}:t>".format(int(datetime.datetime.now().timestamp())), color=0xff0000)
    
    embed.add_field(name="Benzin", value=list[0], inline=True)
    embed.add_field(name="Mazot", value=list[1], inline=True)
    embed.add_field(name="Otogaz", value=list[3], inline=True)
    return embed

@bot.event
async def on_ready():
    global stopper
    stopper = 0
#    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
#    print('--------------------------------------------')
#    print(datetime.datetime.now())
    log.Startup(bot.user, bot.user.id)
    kalan_gun.start()
    await bot.tree.sync()

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.guild is None and not message.author.bot:
        channel = bot.get_channel(int(os.getenv('DM_CHANNEL')))
        await channel.send(f"User: {message.author.display_name} \n{message.content}")
    
    if contains_word(message.content.lower(), "sa") and not  message.author.bot:
        await message.channel.send("as")
    
    if contains_word(message.content.lower(), "ney") and not  message.author.bot:
        await message.channel.send(file=discord.File(img_response["ney"]))
    
    if contains_word(message.content.lower(), ":gabe:") and not  message.author.bot:
        await message.channel.send(file=discord.File(img_response["gabe"]))
    
    #await kufur_kontrol(message, message.author)
    await bot.process_commands(message)

async def kufur_kontrol(message, user):
    global badwords
    msg = message.content.lower()
    user = message.author
    if user.id == 1151874908842893452:
        return
    for word in badwords:
        if word in msg:
            if contains_word(msg, word):
                channel = bot.get_channel(int(os.getenv('LOG_CHANNEL')))
                channel_2 = bot.get_channel(int(os.getenv('LOG_CHANNEL_2')))
                embed=discord.Embed(title="Küfür Kaydı", color=0xff0000)
                embed.add_field(name="Kullanıcı", value = message.author, inline=True)
                embed.add_field(name="Kanal", value = message.channel, inline=True)
                embed.add_field(name="Mesaj", value = message.content, inline=False)
                embed.add_field(name="Yasaklı Kelime", value = word, inline=True)
                embed.add_field(name="Tarih", value=str(datetime.datetime.now()), inline=True)
                await channel.send(embed=embed)
                await channel_2.send(embed=embed)
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
    if (datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 30):
        today = datetime.date.today()
        future = datetime.date(2024, 1, 19)
        diff = future - today
        channel = bot.get_channel(int(os.getenv('DAILY_CHANNEL')))
        log.INFO("Sent daily message")
        await channel.send('{0} gün kaldı.'.format(str(diff)[:2]))


@bot.hybrid_command()
async def add(ctx, left: int, right: int):
    """İki sayıyı toplar. (add <sayı> <sayı>)"""
    await ctx.send(left + right)

@bot.hybrid_command()
async def çevir(ctx, istek: str, hedef: str):
    """Verilen metinleri çevirir."""
    translated = GoogleTranslator(source='auto', target=hedef).translate(text=istek)  
    await ctx.send(translated)


@bot.hybrid_command(pass_context=True)
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.hybrid_command()
async def karaliste_ekle(ctx, kelime: str):
    """Karalisteye kelime ekler."""
    global badwords
    with open('karaliste.txt', 'a') as f:
        f.write("{0}\n".format(kelime))
    with open('karaliste.txt', 'r') as f:
        words = f.read()
        badwords = words.splitlines()
    log.INFO("Added {0} to blacklist.".format(kelime))
    await ctx.send("Eklendi!")
 
@bot.hybrid_command()
async def hızlı(ctx, rp: str ):
    """   Hızlı yanıt modu. (hızlı <mesaj>)"""
    await ctx.send(response[rp])

@bot.hybrid_command()
async def hızlı_ekle(ctx, name: str , tmp: str):
    """Hızlı yanıt moduna kelimeler ekler."""
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
    log.INFO("Sending: "+ path)
    await ctx.send(file=discord.File(path))


@bot.hybrid_command()
async def alper(ctx, istek: str):
    if ( ctx.guild.id == 1122457879660724265):
        """Alperin söylediği efsane şarkıları yollar. (pepe, kısa, uzun)""",
        mp3file = "./alper_{}.mp3".format(istek)
        log.INFO("Sending: " + mp3file)
        await ctx.send(file=discord.File(mp3file))
    else:
        await ctx.send("Bilinmeyen Komut")

@bot.hybrid_command()
async def repeat(ctx, times: int, *, content):
    """Bir mesajı tekrarlar. (repeat <miktar> <mesaj>)"""
    global stopper
    if stopper:
        stopper = False
    if times > 300:
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
async def borsa(ctx):
    """Borsa durumunu gönderir."""
    await ctx.send(embed=fiyatlar())

@bot.hybrid_command()
async def akaryakıt(ctx):
    """Akaryakıt fiyatlarını gönderir."""
    await ctx.send(embed=benzin_fiyat())

@bot.hybrid_command()
async def dur(ctx):
    """Repeat komutunu durdurur."""
    global stopper
    stopper = True

@bot.hybrid_command()
async def resim(ctx, *, resim):
    """İsmi verilen resmi gönderir"""
    log.INFO("Sending: {}".format(resim))
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
    log.INFO("Sending: Shitpost " + patsp)
    await ctx.send(file=discord.File(patsp))

@bot.hybrid_command()
async def hl_shitpost(ctx):
    """Rastgele bir Half-Life shitpostu gönderir."""
    selected_hl = random.choice(hl_shitposts)
    pathl = os.path.join("./hl1", selected_hl)
    log.INFO("Sending: "+ pathl)
    await ctx.send(file=discord.File(pathl))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Bilinmeyen komut: {0}".format(ctx.message.content))
        log.ERROR("Unknown Command: {0}".format(ctx.message.content))

bot.run(os.getenv('TOKEN'), log_handler=None)
