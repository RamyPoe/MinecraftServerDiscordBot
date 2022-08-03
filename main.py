import os
import discord
from discord.ext import commands
from mcstatus import JavaServer as MinecraftServer
import base64
import time
import keep_alive

my_secret = "YOUR_KEY_GOES_HERE"

client = commands.Bot(command_prefix = ',')
client.remove_command('help')
game = discord.Game('with ,help')

fallback = False

def mods(ip):
    server = MinecraftServer.lookup(ip)
    status = server.status()

    mods = []
    
    if 'modinfo' in status.raw:
        for i in status.raw['modinfo']['modList']:
            v = i.items()
            mods.append(i['modid'])
        final = ''
        for i in mods:
            final += f"{i}, "
    else:
        return 'No mods present...'

    return final[:-1]

def download(ip):
    global fallback
    try:
        # print(ip)
        server = MinecraftServer.lookup(str(ip))
        print(ip)
        status = server.status()
        # print(status)
        imgstring = status.favicon
        
        imgstring = imgstring[22:]
        imgdata = base64.b64decode(imgstring)
        filename = 'a.jpg'
        try:
            os.remove('a.jpg')
        except:
            pass
        time.sleep(0.5)
        with open(filename, 'wb') as f:
            f.write(imgdata)
        fallback = False
    except:
        fallback = True

@client.event
async def on_ready():
    await client.change_presence(activity=game)
    print(f'{client.user} is online!')

@client.command()
async def help(ctx):
    embed=discord.Embed(title=",help", description="Shows this menu", color=0xcc3342)
    embed.set_author(name="BOT COMMANDS")
    embed.add_field(name=',server_status', value='Usage: ,server_status [minecraft ip]', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def server_status(ctx, ip):
    global fallback
    try:
        server = MinecraftServer.lookup(ip)
        status = server.status()

        embed=discord.Embed(color=0x5cb85c)
        embed.set_author(name=ip)
        embed.add_field(name='Latency', value=f"{status.latency}ms", inline=False)
        embed.add_field(name='Version', value=status.version.name, inline=False)
        embed.add_field(name='Players', value=f"{status.players.online}/{status.players.max}", inline=False)
        modds = mods(ip)
        if modds:
            embed.add_field(name='Mods', value=modds, inline=False)
        else:
            embed.add_field(name='Mods', value='No mods present...', inline=False)
        download(ip)
        time.sleep(0.1)
        if not fallback:
            file = discord.File("a.jpg", filename="image.jpg")
            embed.set_thumbnail(url="attachment://image.jpg")
        else:
            file = discord.File("b.png", filename="image.png")
            embed.set_thumbnail(url="attachment://image.png")

        await ctx.send(file=file, embed=embed)
    except Exception as e:
        print(e)
        await ctx.send('Invalid ip or server is offline')

keep_alive.keep_alive()
client.run(my_secret)
