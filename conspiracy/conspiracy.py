import discord
from discord.ext import commands, tasks
import asyncio
import time
from time import gmtime, strftime
import datetime
import requests
import json
from TenorFunctions.Tenor import Tenor
client = commands.AutoShardedBot(command_prefix = '!')


@client.event
async def on_ready():
  post_gif.start() # start background processes

@tasks.loop(seconds=60)
async def post_gif():
    current_time = strftime("%H:%M", gmtime())
    if(current_time == '12:00'): # 7am CST
      try: 
        morning_update = Tenor()
        await morning_update.update_morning_gif_file()

        with open('cogs/gif_files/gifs.json', 'r') as gifsFile:
          gif_urls = json.load(gifsFile)
        gif_url = gif_urls["results"][0]["url"] # first gif from file

        general = client.get_channel(400922653218570254) # post gif to channel
        await general.send(gif_url)
      except Exception as e:
        print(e)

# load cogs
extensions = ['GuildGifsAndMessages', 'AnimalGifs']
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