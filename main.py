import discord
import asyncio
from mutagen.mp3 import MP3
from discord.ext.commands import Bot
from discord.ext import commands

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)


@client.command(pass_context=True)
async def clear(ctx, number):
    messages = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit=number):
        messages.append(x)
    await client.delete_messages(messages)


@client.command(pass_context=True)
async def oida(ctx):
    channel = ctx.message.channel
    await client.send_message(channel, "Bist behindat potzn?")


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


@client.command(pass_context=True)
async def do(ctx):
    try:
        channel = ctx.message.author.voice.voice_channel
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player("./audio/the_way.mp3")
        player.start()
        counter = 0
        duration = MP3("./audio/the_way.mp3").info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await client.voice_client_in(server).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


@client.command(pass_context=True)
async def noway(ctx):
    try:
        channel = ctx.message.author.voice.voice_channel
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player("./audio/noway.mp3")
        player.start()
        counter = 0
        duration = 1.05
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await client.voice_client_in(server).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


@client.command(pass_context=True)
async def inthebag(ctx):
    try:
        channel = ctx.message.author.voice.voice_channel
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player("./audio/sky_inthebag.mp3")
        player.start()
        counter = 0
        duration = MP3("./audio/sky_inthebag.mp3").info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await client.voice_client_in(server).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


@client.command(pass_context=True)
async def uready(ctx):
    try:
        channel = ctx.message.author.voice.voice_channel
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player("./audio/accept.mp3")
        player.start()
        counter = 0
        duration = MP3("./audio/accept.mp3").info.length
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        server = ctx.message.server
        await client.voice_client_in(server).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))


@client.command(pass_context=True)
async def kebap(ctx):
    channel = ctx.message.channel
    await client.send_message(channel, "You have gained a <:kebap:418534975831277589>")


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(discord.Object(id='418535433144893440'),
                              "Hello my fellow <:kebap:418534975831277589> eaters")
    # , tts=True


client.run("NDE4NDc2NjcwMTU3MzI0Mjg4.DXiISA.W0cNVm0V4Hv4UgbwFStMqejIZKk")

# add kebap stats
