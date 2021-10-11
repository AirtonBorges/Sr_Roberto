import discord
import os
from discord.ext import commands

ROBERTO_KEY = os.getenv('ROBERTO_KEY')

client = commands.Bot(command_prefix=['<:strawHat_Pepe:632411513990152223> ', '<:strawHat_Pepe:632411513990152223>', ">"])

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(ROBERTO_KEY)