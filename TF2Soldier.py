# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random
import os
import aiohttp
import http.client
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='.tf2 ', description=description, intents=intents)

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

filenames = os.listdir("/home/container/memes/")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)
 

@bot.command()
async def meme(ctx):
    selected_file = random.choice(filenames)
    path = os.path.join("/home/container/memes/", selected_file)

    await ctx.send(file=discord.File(path))



@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        

@bot.command()
async def ping(ctx):
    """Ping"""
    await ctx.send("pong")
    
@bot.command()
async def namaz(ctx):
    """Bot Status"""
    await ctx.send(pp_json(namazvakit()))


bot.run('MTEzODE5NTA4NjI3NDk5ODMxMg.GsEk4L.VgyHh5T33tR7YVK9ePpFMClETANYeZheGmiHbI')
