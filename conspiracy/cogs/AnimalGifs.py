import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from pathlib import Path
import requests
import json
from TenorFunctions.Tenor import Tenor

class AnimalGifs (commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  # Random Cat Gifs
  async def cat(self, ctx):
    tenor = Tenor()
    cat_gif = await tenor.return_gif_from_search("cat")
    await ctx.send(cat_gif)
  
  @commands.command()
  # Random Dog Gifs
  async def dog(self, ctx):
    tenor = Tenor()
    dog_gif = await tenor.return_gif_from_search("dog")
    await ctx.send(dog_gif)

  @commands.command()
  # Random Fennec Fox Gifs
  async def fennecfox(self, ctx):
    tenor = Tenor()
    fennec_fox_gif = await tenor.return_gif_from_search("fennec fox")
    await ctx.send(fennec_fox_gif)

  @commands.command()
  # Random Panda Gifs
  async def panda(self, ctx):
    tenor = Tenor()
    panda_gif = await tenor.return_gif_from_search("panda")
    await ctx.send(panda_gif)

  # @commands.command()
  # # Random Llama Gifs
  # async def llama(self, ctx):
  #   tenor = Tenor()
  #   llama_gif = await tenor.return_gif_from_search("llama")
  #   await ctx.send(llama_gif)

  @commands.command()
  # Random Alpaca Gifs
  async def alpaca(self, ctx):
    tenor = Tenor()
    alpaca_gif = await tenor.return_gif_from_search("alpaca")
    await ctx.send(alpaca_gif)



def setup(client):
  n = AnimalGifs(client)
  client.add_cog(n)  