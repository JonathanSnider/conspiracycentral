import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from pathlib import Path
import requests
import json

class Cat (commands.Cog):
  def __init__(self, client):
    self.client = client

  async def getGif(self):
    # set the apikey and limit
    apikey = "1WXXQZUOL37A"  # app key
    lmt = 1

    # load the user's anonymous ID from cookies or some other disk storage
    # anon_id = <from db/cookies>

    # ELSE - first time user, grab and store their the anonymous ID
    r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)

    if r.status_code == 200:
      anon_id = json.loads(r.content.decode('utf-8'))["anon_id"]
      # store in db/cookies for re-use later
    else:
      anon_id = ""

    # our test search
    search_term = "cat"

    # get the top 8 GIFs for the search term
    r = requests.get(
      "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, apikey, lmt, anon_id))

    if r.status_code == 200:
      # load the GIFs using the urls for the smaller GIF sizes
      top_8gifs = json.loads(r.content.decode('utf-8'))
      with open('cat_gifs.json', 'w') as outfile:
        json.dump(top_8gifs, outfile)
    else:
      top_8gifs = None

    with open('cat_gifs.json', 'r') as gifsFile:
      gifURLs = json.load(gifsFile)
    return gifURLs["results"][0]["url"]

  @commands.command()
  # Random Cat Gifs
  async def cat(self, ctx):
    catGif = await self.getGif()

    await ctx.send(catGif)

  

def setup(client):
  n = Cat(client)
  client.add_cog(n)    