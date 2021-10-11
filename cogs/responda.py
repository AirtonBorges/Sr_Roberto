import discord 
from random import randint
from utils import time, reaction, search_on_brainly
from discord.ext import commands

class Responda(commands.Cog):
  def __init__(self, client):
      self.client = client
      
  @commands.Cog.listener()
  async def on_ready(self):
    print('Loaded Responda')
  
  @commands.command(alises=['brainly', 'Brainly', 'Responda,', 'Responda:', 'responda,', 'responda:'])
  async def responda(self, ctx, *args):
    await ctx.send(f'Pera já vejo')

    args = list(args)
    print (args)

    # Check to see if user wants the link of the question
    getLink = False
    if args[-1] == "_Link":
        args.pop() # Get rid of the argument
        getLink = True
        print("Get Link")
    
    # Join all the words in the args as a Phrase
    text = ' '
    if None not in args:
        text = ' '.join(args)

    # Get the text that answers the question
    message = search_on_brainly(text, getLink)
    print('RESPOSTA: ', message)

    # Send the answer 
    await ctx.send(f'<:Thonk:633762138040565798>... {message}')
    

def setup(client):
  client.add_cog(Responda(client))