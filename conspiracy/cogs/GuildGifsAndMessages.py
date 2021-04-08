import discord
from discord.ext import commands
from discord.ext.commands import Bot



class GuildGifsAndMessages (commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  # Goodnight Angel Command
  async def gnangel(self, ctx): 
    await ctx.send("<@356227435425169418>\nThis nightly checklist might help ensure you don't forget anything..\n:ballot_box_with_check: change your aoe color \n:ballot_box_with_check: charge your controller \n:ballot_box_with_check: charge your headset \n:ballot_box_with_check: say goodnight to the cat \n:ballot_box_with_check: plan to be nice to Sarge, Opera and Reh \n:ballot_box_with_check: Make weapon power pots\n:ballot_box_with_check: go to bed")
  @commands.command()
  # Psijic Reminders Command
  async def psijic(self, ctx):
    await ctx.send("<@356227435425169418> <@384008963504603137> <@294136074454958081> <@294574889652715520>\nThis psijic checklist might help ensure you don't forget anything..\n:ballot_box_with_check: talk to joseph or celery\n:ballot_box_with_check: examine the map\n:ballot_box_with_check: buff your connection\n:ballot_box_with_check: let angel pay for all the wayshrine traveling\n:ballot_box_with_check: don't farm\n:ballot_box_with_check: tell opera to run and go get the portal\n:ballot_box_with_check: wait for sarge and rehdaun")

  @commands.command()
  # Sarge-specific gif Command
  async def sarge(self, ctx):
    await ctx.send("You dare summon the Overlord <@!294574889652715520>??? https://tenor.com/bduc6.gif")

  @commands.command()
  # Opera-specific gif Command
  async def opera(self, ctx):
    await ctx.send("<@!384008963504603137> https://i.pinimg.com/originals/a4/54/a2/a454a2ba58b7cc078dfab573a60102d6.gif")

  @commands.command()
  # Rehdaun-specific gif Command
  async def reh(self, ctx):
    await ctx.send("<@!294136074454958081> https://tenor.com/bc5px.gif")

  @commands.command()
  # Angel-specific gif Command
  async def angel(self, ctx):
    await ctx.send("<@!356227435425169418> https://media1.tenor.com/images/fcfe4cd18c3040cbc85d903a43132dc4/tenor.gif?itemid=13326985")

  @commands.command()
  # Susan-specific gif Command
  async def susan(self, ctx):
    await ctx.send("<@!718983943420117042> https://i0.wp.com/www.twobuttonsdeep.com/wp-content/uploads/2019/10/giphy-3.gif?resize=300%2C169")

  @commands.command()
  # Elizabeth-specific gif Command
  async def elizabeth(self, ctx):
    await ctx.send("<@!595305430335488002> https://media3.giphy.com/media/1BH8ljpH36CTS00Mcc/source.gif")

  @commands.command()
  # Wasp-specific gif Command
  async def wasp(self, ctx):
    await ctx.send("<@!546432782252113921> https://media0.giphy.com/media/1o1r8TqpUkVCynb5mO/giphy.gif")

  @commands.command()
  # Myth-specific gif Command
  async def myth(self, ctx):
    await ctx.send("<@!88360279594778624> https://i.kym-cdn.com/photos/images/newsfeed/001/799/830/d2a.gif")
    #https://i.kym-cdn.com/photos/images/newsfeed/001/799/830/d2a.gif
  
  @commands.command()
  # Goodnight Opera Command
  async def gnopera(self, ctx):
    await ctx.send("<@!384008963504603137> https://cdn.discordapp.com/attachments/462776840659140651/745990601589391411/unknown.png")
  

def setup(client):
  n = Angel(client)
  client.add_cog(n)    