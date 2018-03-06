from main import client, music


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
async def power(ctx):
    await music(ctx, "./audio/power.mp3")


@client.command(pass_context=True)
async def schub(ctx):
    await music(ctx, "./audio/schub.mp3")
