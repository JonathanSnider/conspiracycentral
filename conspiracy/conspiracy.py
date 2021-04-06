import discord
from discord.ext import commands, tasks
import asyncio
import time
from time import gmtime, strftime
import datetime
import requests
import json
client = commands.AutoShardedBot(command_prefix = '!')
# extensions = ['gif']
# ext_len = len(extensions)
# current_ext = 0
# if __name__ == "__main__":
#   while current_ext < ext_len:
#       client.load_extension('cogs.' + str(extensions[current_ext]))
#       print(extensions[current_ext])
#       current_ext+=1

async def getGif():
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
  search_term = "cat morning"

  # get the top 8 GIFs for the search term
  r = requests.get(
    "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, apikey, lmt, anon_id))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    top_8gifs = json.loads(r.content.decode('utf-8'))
    with open('gifs.json', 'w') as outfile:
      json.dump(top_8gifs, outfile)
  else:
    top_8gifs = None

  with open('gifs.json', 'r') as gifsFile:
    gifURLs = json.load(gifsFile)
  return gifURLs["results"][0]["url"]

@client.event
async def on_ready():
  postGIF.start()

@tasks.loop(seconds=60)
async def postGIF():
    current_time = strftime("%H:%M", gmtime())
    #print(current_time)
    if(current_time == '12:00'):
      try:
        gifURL = await getGif()
        general = client.get_channel(400922653218570254)
        await general.send(gifURL)
      except Exception as e:
        print(e)

extensions = ['cat', 'dog', 'angel', 'santa']
ext_len = len(extensions)
current_ext = 0
if __name__ == "__main__":
  while current_ext < ext_len:
      client.load_extension(str(extensions[current_ext]))
      print(extensions[current_ext])
      current_ext+=1

# Run the bot
with open('tokens.json', 'r') as f:
  jsonInfoData = json.load(f)
TOKEN = jsonInfoData["bot"]
client.run(TOKEN)