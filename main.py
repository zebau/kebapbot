import random
import discord
import asyncio
import os
import logging
from exp import *
from os import listdir
from os.path import isfile
from os.path import join
from mutagen.mp3 import MP3
from discord.ext import commands

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='output.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


async def music(ctx, path):
    try:
        channel = ctx.message.author.voice_channel
        if channel is None:
            await client.send_message(ctx.message.channel, "Schau dasd in an Voice Channel kimst!")
            return False

        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player(path)
        player.start()
        counter = 0
        duration = MP3(path).info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await client.voice_client_in(server).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


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
        await client.send_message(channel, "Playing " + onlymp3files[randomfile][:-4] + "'s in the Bag Sound")

        await music(ctx, path)
    elif hero2 is None:
        path = "./audio/inthebags/" + hero1 + ".mp3"
        if os.path.exists(path):
            channel = ctx.message.channel
            await client.send_message(channel, "Playing " + hero1 + "'s in the Bag Sound")

            await music(ctx, path)
        else:
            channel = ctx.message.channel
            await client.send_message(channel, hero1 + " is koa Hero du pfeiffn\n" + inthebagexp)
    else:
        path = "./audio/inthebags/" + hero1 + " " + hero2 + ".mp3"
        if os.path.exists(path):
            channel = ctx.message.channel
            await client.send_message(channel, "Playing " + hero1 + " " + hero2 + "'s in the Bag Sound")

            await music(ctx, path)
        else:
            channel = ctx.message.channel
            await client.send_message(channel, hero1 + " is koa Hero du pfeiffn\n" + inthebagexp)


@client.command(pass_context=True)
async def inthebag(ctx, hero1=None, hero2=None):
    await inthebags(ctx, hero1, hero2)


@client.command(pass_context=True)
async def clear(ctx, number):
    messages = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit=number):
        messages.append(x)
    await client.delete_messages(messages)


@client.command(pass_context=True)
async def sounds(ctx):
    channel = ctx.message.channel
    await client.send_message(channel, soundsexp)


@client.command(pass_context=True)
async def oida(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
        await client.send_message(member, str(member)[:-5] + "?")
    elif member is member:
        member = ctx.message.author
        await client.send_message(member, "fuck")


@client.command(pass_context=True)
async def volume(ctx, value: int):
        pass


@client.command(pass_context=True)
async def yt(ctx, youtube_url):
    channel = ctx.message.author.voice.voice_channel
    # http://discordpy.readthedocs.io/en/latest/api.html#discord.Member.voice
    # http://discordpy.readthedocs.io/en/latest/api.html#discord.VoiceState.voice_channel
    if youtube_url.startswith('https://www.youtube.com/watch?v='):
        voice = await client.join_voice_channel(channel)
        player = await voice.create_ytdl_player(youtube_url)
        player.start()
        player.volume = 0.6
    else:
        return 'URL_ERROR'


@client.command(ass_context=True)
async def leave(ctx):
    await client.voice_client_in(discord.Object(id="418525123176300544")).disconnect()


@client.command(pass_context=True)
async def kebapold(ctx, kebaps:int = None):
    channel = ctx.message.channel
    if kebaps is None:
        await client.send_message(channel, "Waifü Kebap host den gessn?")
    elif kebaps >= 5:
        await client.send_message(channel, "I moa ned dasd {0} Kebap gessn host, oda?".format(kebaps))
    elif kebaps >= 0:
        await client.send_message(channel, "Host wirklich {0} Kebap gessn?".format(kebaps))
    else:
        await client.send_message(channel, str(kebaps))


# TODO finish ?kebap
@client.command(pass_context=True)
async def kebap(ctx):
    channel = ctx.message.channel
    message = ctx.message

    if message.content.startswith('?kebap'):
        await client.send_message(channel, "Wiavü Kebap host den gessn?")
        kebaps = await client.wait_for_message()
        kebaps = kebaps.content

        if int(kebaps) >= 5:
            await client.send_message(channel, "I moa ned dasd {0} Kebap gessn host, oda?".format(kebaps))

        elif int(kebaps) > 0:
            await client.send_message(channel, "Don post amoi a bild von deim Kebap in #kebaptalk")


@client.event
async def on_message(message):
    await client.process_commands(message)
    if 'kebap' in message.content:
        await client.add_reaction(message, "kebap:418534975831277589")


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=discord.Game(name='with Kebaps'))
    await client.send_message(discord.Object(id='418535433144893440'),
                              "Hello my fellow <:kebap:418534975831277589> eaters")


# TODO make error logs work
# TODO send private messages in my discord server

client.run("NDE4NDc2NjcwMTU3MzI0Mjg4.DXiISA.W0cNVm0V4Hv4UgbwFStMqejIZKk")

# add kebap stats