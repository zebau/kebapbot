import random
import discord
import asyncio
import os
import traceback
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

logging.basicConfig(filename='.\output.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


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
async def leave():
    await client.voice_client_in(discord.Object(id="418525123176300544")).disconnect()


# Sounds
@client.command(pass_context=True)
async def theway(ctx):
    await music(ctx, "./audio/the_way.mp3")


@client.command(pass_context=True)
async def noway(ctx):
    await music(ctx, "./audio/noway.mp3")


@client.command(pass_context=True)
async def skybag(ctx):
    await music(ctx, "./audio/sky_inthebag.mp3")


@client.command(pass_context=True)
async def klassisch(ctx):
    await music(ctx, "./audio/klassischer_lich.mp3")


@client.command(pass_context=True)
async def woasned(ctx):
    await music(ctx, "./audio/i_woas_ned_wos_es_hobts.mp3")


@client.command(pass_context=True)
async def dead(ctx):
    await music(ctx, "./audio/dead_as_hell.mp3")


@client.command(pass_context=True)
async def ezmmr(ctx):
    await music(ctx, "./audio/ez_mmr_with_jogoe_gaming.mp3")


@client.command(pass_context=True)
async def spritzwein(ctx):
    await music(ctx, "./audio/man_bringe_spritzwein.mp3")


@client.command(pass_context=True)
async def dmg(ctx):
    await music(ctx, "./audio/heizakara_i_ho_dmg.mp3")


@client.command(pass_context=True)
async def killingspree(ctx):
    await music(ctx, "./audio/lich_killing_spree.mp3")


@client.command(pass_context=True)
async def aushem(ctx):
    await music(ctx, "./audio/weng_wos_wiad_mi_den_dea_hund_imma_aushem.mp3")


@client.command(pass_context=True)
async def rune(ctx):
    await music(ctx, "./audio/fidi_rune.mp3")


@client.command(pass_context=True)
async def chance(ctx):
    await music(ctx, "./audio/keine_chance.mp3")


@client.command(pass_context=True)
async def danke(ctx):
    await music(ctx, "./audio/lernvideo_danke.mp3")


@client.command(pass_context=True)
async def eingabetaste(ctx):
    await music(ctx, "./audio/lernvideo_eingabetaste.mp3")


@client.command(pass_context=True)
async def oah(ctx):
    await music(ctx, "./audio/lich_oah.mp3")


@client.command(pass_context=True)
async def speim(ctx):
    await music(ctx, "./audio/speim.mp3")


@client.command(pass_context=True)
async def onfire(ctx):
    await music(ctx, "./audio/jogo_on_fire.mp3")


@client.command(pass_context=True)
async def dejavu(ctx):
    await music(ctx, "./audio/dejavu.mp3")


@client.command(pass_context=True)
async def running(ctx):
    await music(ctx, "./audio/90s.mp3")


@client.command(pass_context=True)
async def schub(ctx):
    await music(ctx, "./audio/schub.mp3")
# end of sounds


@client.command(pass_context=True)
async def kebap(ctx, kebaps:int = None):
    channel = ctx.message.channel
    if kebaps is None:
        await client.send_message(channel, "Waifü Kebap host den gessn?")
    elif kebaps >= 5:
        await client.send_message(channel, "I moa ned dasd {0} Kebap gessn host, oda?".format(kebaps))
    elif kebaps >= 0:
        await client.send_message(channel, "Host wirklich {0} Kebap gessn?".format(kebaps))
    else:
        await client.send_message(channel, str(kebaps))


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(discord.Object(id='418535433144893440'),
                              "Hello my fellow <:kebap:418534975831277589> eaters")


@client.event
async def on_error(ctx, event, *args, **kwargs):
    message = args[0]
    logging.warning(traceback.format_exc())
    channel = ctx.message.channel
    await client.send_message(channel, "Error djud!")


    # , tts=True


client.run("NDE4NDc2NjcwMTU3MzI0Mjg4.DXiISA.W0cNVm0V4Hv4UgbwFStMqejIZKk")

# add kebap stats