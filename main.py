import random
import aiohttp
import discord
import asyncio
import os
import logging
from bs4 import BeautifulSoup
from exp import *
from os import listdir
from os.path import isfile, join
from mutagen.mp3 import MP3
from discord.ext import commands



# if not discord.opus.is_loaded():
#     discord.opus.load_opus('opus')
from music import Music

bot_prefix = "?"
bot = commands.Bot(command_prefix=bot_prefix)

# config vars

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='output.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

###
#  db = MySQLdb.connect(host='localhost',
#                    user='root',
#                     db='kebapstats')
#
# cursor = db.cursor()
#
# cursor.execute("SELECT * FROM kebapstats")
#
# db.close()
###


async def music(ctx, path):
    try:
        channel = ctx.message.author.voice_channel
        if channel is None:
            await bot.send_message(ctx.message.channel, "Schau dasd in an Voice Channel kimst!")
            return False
        voice = await bot.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(path)
        player.start()
        counter = 0
        duration = MP3(path).info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await bot.voice_client_in(server).disconnect()
    except Exception as exc:
        await bot.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


async def inthebags(ctx, hero1=None, hero2=None):
    if hero1 is None:
        folderpath = "./audio/inthebags"
        files = [f for f in listdir(folderpath) if isfile(join(folderpath, f))]

        onlymp3files = []
        for f in files:
            if f[-3:] == "mp3":
                onlymp3files.append(f)

        randomfile = random.randint(0, len(onlymp3files)-1)
        path = folderpath + "/" + onlymp3files[randomfile]

        channel = ctx.message.channel
        await bot.send_message(channel, "Playing " + onlymp3files[randomfile][:-4] + "'s in the Bag Sound")

        await music(ctx, path)
    elif hero2 is None:
        path = "./audio/inthebags/" + hero1 + ".mp3"
        if os.path.exists(path):
            channel = ctx.message.channel
            await bot.send_message(channel, "Playing " + hero1 + "'s in the Bag Sound")

            await music(ctx, path)
        else:
            channel = ctx.message.channel
            await bot.send_message(channel, hero1 + " is koa Hero du pfeiffn\n" + inthebagexp)
    else:
        path = "./audio/inthebags/" + hero1 + " " + hero2 + ".mp3"
        if os.path.exists(path):
            channel = ctx.message.channel
            await bot.send_message(channel, "Playing " + hero1 + " " + hero2 + "'s in the Bag Sound")

            await music(ctx, path)
        else:
            channel = ctx.message.channel
            await bot.send_message(channel, hero1 + " is koa Hero du pfeiffn\n" + inthebagexp)


@commands.command(pass_context=True)
async def inthebag(ctx, hero1=None, hero2=None):
    await inthebags(ctx, hero1, hero2)


@commands.command(pass_context=True)
async def clear(ctx, number):
    messages = []
    number = int(number)
    async for x in bot.logs_from(ctx.message.channel, limit=number):
        messages.append(x)
    await bot.delete_messages(messages)


@commands.command(pass_context=True)
async def sounds(ctx):
    channel = ctx.message.channel
    await bot.send_message(channel, soundsexp)


@commands.command(pass_context=True)
async def oida(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
        await bot.send_message(member, str(member)[:-5] + "?")
    elif member is member:
        member = ctx.message.author
        await bot.send_message(member, "fuck")


@commands.command(pass_context=True)
async def volume(ctx, value: int):
        pass


@commands.command(pass_context=True)
async def yt(ctx, youtube_url):
    channel = ctx.message.author.voice.voice_channel
    # http://discordpy.readthedocs.io/en/latest/api.html#discord.Member.voice
    # http://discordpy.readthedocs.io/en/latest/api.html#discord.VoiceState.voice_channel
    if youtube_url.startswith('https://www.youtube.com/watch?v='):
        voice = await bot.join_voice_channel(channel)
        player = await voice.create_ytdl_player(youtube_url)
        player.start()
        player.volume = 0.6
    else:
        return 'URL_ERROR'


@commands.command(ass_context=True)
async def leave():
    try:
        await bot.voice_client_in(discord.Object(id="418525123176300544")).disconnect()
    except Exception as exc:
        await bot.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


# TODO finish ?kebap
@commands.command(pass_context=True)
async def kebap(ctx):
    channel = ctx.message.channel
    message = ctx.message

    if message.content.startswith('?kebap'):
        await bot.send_message(channel, "Wiavü Kebap host den gessn?")
        kebaps = await bot.wait_for_message()
        kebaps = kebaps.content

        if int(kebaps) >= 5:
            await bot.send_message(channel, "I moa ned dasd {0} Kebap gessn host, oda?".format(kebaps))
            kebapanswer = await bot.wait_for_message()
            kebapanswer = kebapanswer.content
            if kebapanswer.startswith('y') or kebapanswer.startswith('doch'):
                await bot.send_message(channel, "Schau dasd weida kimmst")
            elif kebapanswer.startswith('na'):
                await bot.send_message(channel, "I moa hoid a")
            else:
                pass
        elif int(kebaps) > 0:
            await bot.send_message(channel, "Don post amoi a bild von deim Kebap in #kebaptalk")


# @bot.event
# async def on_message(message):
#    await bot.process_commands(message)
#    if 'kebap' in message.content:
#       await bot.add_reaction(message, "kebap:418534975831277589")


@commands.command(pass_context=True)
async def dotanow(self):
    url = "https://steamdb.info/app/570/graphs/"
    async with aiohttp.get(url) as response:
        soupObject = BeautifulSoup(await response.text(), "html.parser")
    try:
        online = soupObject.find(class_='steamspy-stats').find('li').find('strong').get_text()
        await self.bot.say(online + ' dudes spün grod dotes')
    except:
        await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")


@commands.command(pass_context=True)
async def csgonow(self):
    url = "https://steamdb.info/app/730/graphs/"
    async with aiohttp.get(url) as response:
        soupObject = BeautifulSoup(await response.text(), "html.parser")
    try:
        online = soupObject.find(class_='steamspy-stats').find('li').find('strong').get_text()
        await self.bot.say(online + ' dudes dreschn grod russn')
    except:
        await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(game=discord.Game(name='with Kebaps'))

# TODO make error logs work
# TODO send private messages in my discord server


bot.add_cog(Music(bot))
bot.run("")

# add kebap stats