import discord
from discord.ext import commands, tasks
import asyncio
import time
from time import gmtime, strftime
import datetime
import requests
import json
client = commands.AutoShardedBot(command_prefix = '!')

async def update_gif_file(): # update the gif file with new gifs
  # set the api key and limit
  with open('tokens.json', 'r') as f:
    tokens = json.load(f)  # app key
  API_KEY = tokens["tenor"]
  lmt = 1

  # load the user's anonymous ID from cookies or some other disk storage

  # ELSE - first time user, grab and store their the anonymous ID
  r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % API_KEY)

  if r.status_code == 200:
    anon_id = json.loads(r.content.decode('utf-8'))["anon_id"]
  else:
    anon_id = ""

  # search term
  search_term = "cat morning"

  # get the top 8 GIFs for the search term
  r = requests.get(
    "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, API_KEY, lmt, anon_id))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    top_8gifs = json.loads(r.content.decode('utf-8'))
    with open('gifs.json', 'w') as outfile:
      json.dump(top_8gifs, outfile)
  else:
    top_8gifs = None


@client.event
async def on_ready():
  post_gif.start() # start background processes

@tasks.loop(seconds=60)
async def post_gif():
    current_time = strftime("%H:%M", gmtime())
    if(current_time == '12:00'): # 7am CST
      try: 
        await update_gif_file()

        with open('gifs.json', 'r') as gifsFile:
          gif_urls = json.load(gifsFile)
        gif_url = gif_urls["results"][0]["url"] # first gif from file

        general = client.get_channel(400922653218570254) # post gif to channel
        await general.send(gif_url)
      except Exception as e:
        print(e)

# load cogs
extensions = ['cat', 'dog', 'GuildGifsAndMessages', 'santa']
ext_len = len(extensions)
current_ext = 0
for cog in extensions:
  try:
    client.load_extension(f"cogs.{cog}")
    print(f"{cog} was successfully loaded!")
  except Exception as e:
    print(f"There was an error loading {cog}: {e}")

# Run the bot
with open('tokens.json', 'r') as f:
  tokens = json.load(f)
TOKEN = tokens["bot"]
client.run(TOKEN)