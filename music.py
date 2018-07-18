import random
import aiohttp
import discord
import asyncio
import os
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from mutagen.mp3 import MP3
from discord.ext import commands


# if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
#     discord.opus.load_opus('opus')

# config vars
file = open('TOKEN.txt', 'r')
BOT_TOKEN = file.read().strip()
file.close()


async def music(ctx, path):
    try:
        channel = ctx.message.author.voice_channel
        server = ctx.message.server
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
        if bot.voice_client_in(server):
            await bot.voice_client_in(server).disconnect()
        else:
            pass

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


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Music:

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel: discord.Channel):
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await self.bot.say('This is not a voice channel...')
        else:
            await self.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def leave(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            del self.voice_states[server.id]
            state.audio_player.cancel()
            await state.voice.disconnect()
            await bot.voice_client_in(server).disconnect()
        except:
            await bot.voice_client_in(server).disconnect()


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))


    @commands.command(pass_context=True)
    async def reg(self, ctx):
        await music(ctx, "./audio/reg.mp3")

    @commands.command(pass_context=True)
    async def theway(self, ctx):
        await music(ctx, "./audio/the_way.mp3")

    @commands.command(pass_context=True)
    async def noway(self, ctx):
        await music(ctx, "./audio/noway.mp3")

    @commands.command(pass_context=True)
    async def bmrune(self, ctx):
        await music(ctx, "./audio/beast_rune.mp3")

    @commands.command(pass_context=True)
    async def viper(self, ctx):
        await music(ctx, "./audio/holyshitviper.mp3")

    @commands.command(pass_context=True)
    async def spit(self, ctx):
        await music(ctx, "./audio/spit.mp3")

    @commands.command(pass_context=True)
    async def skybag(self, ctx):
        await music(ctx, "./audio/sky_inthebag.mp3")

    @commands.command(pass_context=True)
    async def klassisch(self, ctx):
        await music(ctx, "./audio/klassischer_lich.mp3")

    @commands.command(pass_context=True)
    async def woasned(self, ctx):
        await music(ctx, "./audio/i_woas_ned_wos_es_hobts.mp3")

    @commands.command(pass_context=True)
    @commands.has_role('Crusader')
    async def suh(self, ctx):
        await music(ctx, "./audio/suh.mp3")

    @commands.command(pass_context=True)
    async def dead(self, ctx):
        await music(ctx, "./audio/dead_as_hell.mp3")

    @commands.command(pass_context=True)
    async def ezmmr(self, ctx):
        await music(ctx, "./audio/ez_mmr_with_jogoe_gaming.mp3")

    @commands.command(pass_context=True)
    async def spritzwein(self, ctx):
        await music(ctx, "./audio/man_bringe_spritzwein.mp3")

    @commands.command(pass_context=True)
    async def dmg(self, ctx):
        await music(ctx, "./audio/heizakara_i_ho_dmg.mp3")

    @commands.command(pass_context=True)
    async def killingspree(self, ctx):
        await music(ctx, "./audio/lich_killing_spree.mp3")

    @commands.command(pass_context=True)
    async def aushem(self, ctx):
        await music(ctx, "./audio/weng_wos_wiad_mi_den_dea_hund_imma_aushem.mp3")

    @commands.command(pass_context=True)
    async def rune(self, ctx):
        await music(ctx, "./audio/fidi_rune.mp3")

    @commands.command(pass_context=True)
    async def chance(self, ctx):
        await music(ctx, "./audio/keine_chance.mp3")

    @commands.command(pass_context=True)
    async def danke(self, ctx):
        await music(ctx, "./audio/lernvideo_danke.mp3")

    @commands.command(pass_context=True)
    async def eingabetaste(self, ctx):
        await music(ctx, "./audio/lernvideo_eingabetaste.mp3")

    @commands.command(pass_context=True)
    async def oah(self, ctx):
        await music(ctx, "./audio/lich_oah.mp3")

    @commands.command(pass_context=True)
    async def onfire(self, ctx):
        await music(ctx, "./audio/jogo_on_fire.mp3")

    @commands.command(pass_context=True)
    async def dejavu(self, ctx):
        await music(ctx, "./audio/dejavu.mp3")

    @commands.command(pass_context=True)
    async def running(self, ctx):
        await music(ctx, "./audio/90s.mp3")

    @commands.command(pass_context=True)
    async def power(self, ctx):
        await music(ctx, "./audio/power.mp3")

    @commands.command(pass_context=True)
    async def schub(self, ctx):
        await music(ctx, "./audio/schub.mp3")

    @commands.command(pass_context=True)
    async def speim(self, ctx):
        await music(ctx, "./audio/speim.mp3")

    @commands.command(pass_context=True)
    async def toto(self, ctx):
        await music(ctx, "./audio/toto.mp3")

    @commands.command(pass_context=True)
    async def berni(self, ctx):
        await music(ctx, "./audio/berni.mp3")

    @commands.command(pass_context=True)
    async def inthebag(self, ctx, hero1=None, hero2=None):
        await inthebags(ctx, hero1, hero2)

    @commands.command(pass_context=True)
    async def aleave(self):
        try:
            await bot.voice_client_in(discord.Object(id="418525123176300544")).disconnect()
        except Exception as exc:
            await bot.send_message(discord.Object(id='418814283036491776'), "Error: ```{ttt}```".format(ttt=exc))
    @commands.command(pass_context=True)
    async def dotanow(self):
        url = "https://steamdb.info/app/570/graphs/"
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            online = soupObject.find(class_='steamspy-stats').find('li').find('strong').get_text()
            await self.bot.say(online + ' dudes spün grod dotes')
        except:
            await self.bot.say(
                "Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @commands.command(pass_context=True)
    async def csgonow(self):
        url = "https://steamdb.info/app/730/graphs/"
        async with aiohttp.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            online = soupObject.find(class_='steamspy-stats').find('li').find('strong').get_text()
            await self.bot.say(online + ' dudes dreschn grod russn')
        except:
            await self.bot.say(
                "Couldn't load amount of players. No one is playing this game anymore or there's an error.")

    @commands.command(pass_context=True)
    async def clear(self, ctx, number):
        messages = []
        number = int(number)
        async for x in bot.logs_from(ctx.message.channel, limit=number):
            messages.append(x)
        await bot.delete_messages(messages)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='sounds bois')
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await bot.change_presence(game=discord.Game(name='with Kebaps'))


bot.run(BOT_TOKEN)

