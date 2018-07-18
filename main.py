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


###
# @commands.command(pass_context=True)
# async def kebap(ctx):
#    channel = ctx.message.channel
#    message = ctx.message
#
#   if message.content.startswith('?kebap'):
#       await bot.send_message(channel, "Wiavü Kebap host den gessn?")
#       kebaps = await bot.wait_for_message()
#       kebaps = kebaps.content
#
#       if int(kebaps) >= 5:
#           await bot.send_message(channel, "I moa ned dasd {0} Kebap gessn host, oda?".format(kebaps))
#           kebapanswer = await bot.wait_for_message()
#           kebapanswer = kebapanswer.content
#           if kebapanswer.startswith('y') or kebapanswer.startswith('doch'):
#               await bot.send_message(channel, "Schau dasd weida kimmst")
#           elif kebapanswer.startswith('na'):
#              await bot.send_message(channel, "I moa hoid a")
#           else:
#              pass
#       elif int(kebaps) > 0:
#          await bot.send_message(channel, "Don post amoi a bild von deim Kebap in #kebaptalk")
#

#    -- add reaction on message
# @bot.event
# async def on_message(message):
#    await bot.process_commands(message)
#    if 'kebap' in message.content:
#       await bot.add_reaction(message, "kebap:418534975831277589")
#
