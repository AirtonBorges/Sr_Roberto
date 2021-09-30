import discord 
from random import randint
from utils import time, reaction
from discord.ext import commands

class Opa(commands.Cog):
  def __init__(self, client):
      self.client = client
      
  @commands.Cog.listener()
  async def on_ready(self):
    print('Loaded Opa')
  
  @commands.command(aliases=[f'{"o" * o}pa' for o in range(2, 100)])
  async def opa(self, ctx, *args):
    # uses an list of opa to make so the user can use a lot of o's
    le = time()['letra']
    pa = time()['periodo']

    # if the number of letters is more than 2000, the bot just pics a new random number of letters to display

    # multiply a [letra] of the [periodo] by that random number to make it look like is an old person answering
    pl = pa.split(le, 1)
    size = ctx.message.content.count(le)
    pl.insert(1, le * ((size + 1) + (randint(-size, size))))
    pl = ''.join(pl)

    await ctx.send(f"{pl} {reaction(*args)}")      


def setup(client):
  client.add_cog(Opa(client))