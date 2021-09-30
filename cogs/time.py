import discord 
from random import randint
from utils import time, reaction
from discord.ext import commands

class Time(commands.Cog):
  def __init__(self, client):
      self.client = client
      
  @commands.Cog.listener()
  async def on_ready(self):
    print('Loaded Time')
  
  @commands.command(aliases=['horas', 'Horas', 'Hora', 'hora'])
  async def time(self, ctx, *args):
    await ctx.send(f'{reaction(*args)} São {time()["hora"]}')

def setup(client):
  client.add_cog(Time(client))