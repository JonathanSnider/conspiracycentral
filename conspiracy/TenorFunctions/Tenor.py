import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from pathlib import Path
import requests
import json




class Tenor (commands.Cog):
  def __init__(self, client):
    self.client = client

  async def update_morning_gif_file(self): # update the gif file with new gifs
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
      with open('gif_files/gifs.json', 'w') as outfile:
        json.dump(top_8gifs, outfile)
    else:
      top_8gifs = None

  async def return_gif_from_search(self, search_term):
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
    
    # get the top 8 GIFs for the search term
    r = requests.get(
      "https://api.tenor.com/v1/random?q=%s&key=%s&limit=%s&anon_id=%s" % (search_term, API_KEY, lmt, anon_id))

    if r.status_code == 200:
      # load the GIFs using the urls for the smaller GIF sizes
      top_8gifs = json.loads(r.content.decode('utf-8'))
      with open(f'gif_files/random_animal_gifs.json.json', 'w') as outfile:
        json.dump(top_8gifs, outfile)
    else:
      top_8gifs = None

    with open('gif_files/random_animal_gifs.json.json', 'r') as gifs_file:
      gif_urls = json.load(gifs_file)
    return gif_urls["results"][0]["url"]

def setup(client):
  n = Tenor(client)
  client.add_cog(n)  