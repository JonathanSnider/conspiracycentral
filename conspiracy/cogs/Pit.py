import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import json
from pathlib import Path
import sqlite3

class Pit (commands.Cog):
  def __init__(self, client):
    self.client = client

  async def add_roles_to_db(self, pitted_person_id, pitted_person_roles):
    conn = sqlite3.connect('dbs/pitted.db')
    c = conn.cursor()

    sql = "INSERT INTO pitted VALUES(?,?)"
    c.execute(sql,(pitted_person_id, pitted_person_roles))

    conn.commit()
    c.close()
    conn.close()

  async def return_roles_and_remove_from_db(self, pitted_person_id):
    conn = sqlite3.connect('dbs/pitted.db')
    c = conn.cursor()

    sql = "SELECT pitted_roles FROM pitted WHERE pitted_id = ?"
    c.execute(sql,(pitted_person_id,))
    pitted_roles = c.fetchone()
    
    if(pitted_roles != None): # not a person saved with that ID
      sql = "DELETE FROM pitted WHERE pitted_id = ?"
      c.execute(sql,(pitted_person_id,))
    
    conn.commit()
    c.close()
    conn.close()
    return pitted_roles

  @commands.command()
  async def pit(self, ctx):
    msg_author = ctx.message.author
    with open('tokens.json') as f:
      tokens = json.load(f)
    user_ids = tokens["user_ids"]

    if(str(msg_author.id) not in [user_ids["sarge"], user_ids["angel"]]):
      unlucky_bastard = msg_author # person trying to pit without permission
      await unlucky_bastard.send("https://tenor.com/OySq.gif")
    else:
      unlucky_bastard = ctx.message.mentions[0]
    try:
      pit_role = discord.utils.get(ctx.message.guild.roles, name="The Pit")
      user_roles = [y.name for y in unlucky_bastard.roles][1:] # first is @everyone
      user_roles_str = ",".join(user_roles[0:]) # comma is for a delimiter
      
      await self.add_roles_to_db(str(unlucky_bastard.id), user_roles_str)

      for role in user_roles:
        role_to_remove = discord.utils.get(ctx.message.guild.roles, name=role)
        try: # just in case a role is higher than it
          await unlucky_bastard.remove_roles(role_to_remove, reason="Pitted")
        except Exception as e:
          await ctx.send(f"There was an error: {e}")

      await unlucky_bastard.add_roles(pit_role, reason="Pitted")
    except Exception as e:
      await ctx.send(f"There was an error: {e}")

  @commands.command()
  async def unpit(self, ctx):
    msg_author = ctx.message.author
    with open('tokens.json') as f:
      tokens = json.load(f)
    user_ids = tokens["user_ids"]
    general_channel_id = int(tokens["channel_ids"]["general"])

    if(str(msg_author.id) not in [user_ids["sarge"], user_ids["angel"]]):
      await ctx.send("https://tenor.com/OySq.gif") # person trying to unpit without permission
    else:
      try:
        user_mentioned = ctx.message.mentions[0]
        pit_role = discord.utils.get(ctx.message.guild.roles, name="The Pit")
        pitted_roles = await self.return_roles_and_remove_from_db(str(user_mentioned.id))
        if(pitted_roles == None):
          await ctx.send("No one pitted with that ID")
          return # no one pitted with ID given, end command
        else:
          pitted_roles_list = pitted_roles[0].split(',')
          await user_mentioned.remove_roles(pit_role, reason="Unpitted")
          for role_name in pitted_roles_list:
            role_to_add = discord.utils.get(ctx.message.guild.roles, name=role_name)
            try: # just in case a role is higher than it
              await user_mentioned.add_roles(role_to_add, reason="Unpitted")
            except Exception as e:
              await ctx.send(f"There was an error: {e}")

          
          general_channel = self.client.get_channel(general_channel_id)
          await general_channel.send(f"https://giphy.com/gifs/clint-eastwood-1971-c2pOELjarKcU \n <@{user_mentioned.id}>")
          await ctx.message.delete()

      except Exception as e:
        await ctx.send(f"There was an error: {e}")

        


def setup(client):
  n = Pit(client)
  client.add_cog(n)   