import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)


@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.send_message(discord.Object(id='418535433144893440'),
                              "Hello my fellow <:kebap:418534975831277589> eaters")
    # , tts=True


@client.command(pass_context=True)
async def clear(ctx, number):
    messages = []
    number = int(number)
    async for x in client.logs_from(ctx.message.channel, limit=number):
        messages.append(x)
    await client.delete_messages(messages)


@client.command(pass_context=True)
async def do():
    try:
        channel = client.get_channel("418526534165594114")
        voice = await client.join_voice_channel(channel)
        player = voice.create_ffmpeg_player("./audio/the_way.mp3")
        player.start()
        counter = 0
        duration = 1
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        await client.voice_client_in(discord.Object(id="418525123176300544")).disconnect()
    except Exception as exc:
        await client.send_message(discord.Object(id='418475702321676299'),
                                  "Es ist ein Fehler aufgetreten. ```{ttt}```".format(ttt=exc))


client.run("NDE4NDc2NjcwMTU3MzI0Mjg4.DXiISA.W0cNVm0V4Hv4UgbwFStMqejIZKk")
