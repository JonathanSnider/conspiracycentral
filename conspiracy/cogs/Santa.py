# Secret Sanat

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from pathlib import Path
import requests
import json
import random

class Santa (commands.Cog):
  def __init__(self, client):
    self.client = client

  async def check_if_in_file(self, name, user_id):
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)

    for user_name, Id in people.items():
      if(user_name == name):
        return True
      elif(user_id == Id): # user updated name
        removed_person = await self.delete_user_from_file(user_name) 
        return False
    return False

  async def put_user_in_file(self, name, user_id):
    new_value = {name: user_id}
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)

    people.update(new_value)

    with open("people.json", 'w') as out_file:
      json.dump(people, out_file)

  async def delete_user_from_file(self, name):
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)
    removed_person = people.pop(name, None)
    with open("people.json", 'w') as out_file:
      json.dump(people, out_file)    
    return removed_person

  async def prune_users(self):
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)

    name_list = []
    id_list = []

    for user_name, user_id in people.items():
      if(user_name in name_list):
        removed_person = await self.delete_user_from_file(user_name)
      elif(user_id in id_list):
        removed_person = await self.delete_user_from_file(user_name)
      else:
        name_list.append(user_name)
        id_list.append(user_id)

  async def get_random_person(self, name_list):
    return random.choice(name_list)

  async def get_random_pairs(self):
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)

    with open('tokens.json') as f:
      tokens = json.load(f)
    user_ids = tokens["user_ids"]

    name_list = []
    for name in people:
      name_list.append(name)

    random_pairs = []
    already_picked = []
    already_picked_ids = []
    for name in name_list:
      valid_pick = False
      while not valid_pick:
        pick = await self.get_random_person(name_list)
        if(len(name_list) > 5) and ((people[name] == int(user_ids["myth"]) and people[pick] == int(user_ids["chummy"])) or (people[name] == int(user_ids["chummy"]) and people[pick] == int(user_ids["myth"]))): # myth and chummy case
          if(len(name_list) == (len(already_picked) + 2)):
            if(int(user_ids["myth"]) not in already_picked_ids) and (int(user_ids["chummy"]) not in already_picked_ids):
              return False
        else:
          if(pick in already_picked):
            pass # not valid pick
          elif(name == pick): # cant pick yourself
            if(len(name_list) == (len(already_picked) + 1)):
              return False
            else:
              pass # not a valid pick
          else:
            already_picked.append(pick)
            already_picked_ids.append(people[pick])
            valid_pick = True # valid pick
      pair = name, pick
      random_pairs.append(pair)
    return random_pairs
  
  async def message_pairs(self, ctx, namePairs):
    with open("people.json", 'r') as in_file:
      people = json.load(in_file)
    for names in namePairs:
      user_to_message = await ctx.guild.fetch_member(people[names[0]])
      await user_to_message.send(f"Hello there {names[0]}! Your Secret Santa pick is **{names[1]}**. Have a good day and Merry Christmas!")

  @commands.command()
  # Enter Command
  async def enter(self, ctx):
    name = ctx.author.name
    user_id = ctx.author.id
    user_in_file = await self.check_if_in_file(name, user_id)
    
    if(user_in_file == True):
      await ctx.send("Already entered!")
      return
    else:
      try:
        await self.put_user_in_file(name, user_id)
        await ctx.send("Entered!")
      except Exception as e:
        await ctx.send("Sorry! There was an error.")
        await ctx.send(f"<@294574889652715520> {e}")
  
  @commands.command()
  # Withdraw Command
  async def withdraw(self, ctx):
    name = ctx.author.name
    try:
      removed_person = await self.delete_user_from_file(name)
      if(removed_person == None):
        await ctx.send("Not entered! Please use **!enter** to enter yourself!")
      else:
        await ctx.send("Withdrawn!")
    except Exception as e:
      await ctx.send("Sorry! There was an error.")
      await ctx.send(f"<@294574889652715520> {e}")

  @commands.command()
  # Draw picks
  # Can only be used by Rehdaun and Sarge
  async def draw(self, ctx):
    user_id = ctx.author.id
    with open('tokens.json') as f:
      tokens = json.load(f)
    user_ids = tokens["user_ids"]
    if(user_id in [int(user_ids["rehdaun"]), int(user_ids["sarge"])]):
      try:
        await self.prune_users()
        validPicks = False
        while not validPicks:
          pairs = await self.get_random_pairs()
          if(pairs != False):
            validPicks = True
        await self.message_pairs(ctx, pairs)
      except Exception as e:
        await ctx.send("Sorry! There was an error.")
        await ctx.send(f"<@{user_ids['sarge']}> {e}")
    else:
      await ctx.send("https://tenor.com/R0yA.gif")

def setup(client):
  n = Santa(client)
  client.add_cog(n)    