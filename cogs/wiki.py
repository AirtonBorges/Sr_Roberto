from datetime import datetime
from time import sleep
from discord.ext import commands

from utils import time, reaction, requests, TIME_FORMAT, Wikis, Random

class Wiki(commands.Cog):
  def __init__(self, client):
      self.client = client
      self.isRunning = False
      
  @commands.Cog.listener()
  async def on_ready(self):
    print('Loaded Wiki')
  
  @commands.command(aliases=['Aleatorio', 'Wiki_Aleatoria', 'Aleatoria', 'Wikispeedrun'])
  async def aleatoria(self, ctx, *args):
    getRandomPageUrl = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"
    randomPage =  requests.get(getRandomPageUrl).url
    
    await ctx.send(f"{reaction(*args)} Aqui o sua página aleatória: \n\nLink:{randomPage}")

  @commands.command(aliases=['WikiSpeedrun', 'wikiSpeedrun'])
  async def wikispeedrun(self, ctx, *args):
    if self.isRunning:
        await ctx.send("Já tem uma speedRun acontecendo, acaba primeiro antes de ir pra outra <:RAGEY:662481054719803443>")
    else:
        self.isRunning = True

        wikiList = Wikis()
        wikiNames = wikiList.getNames()

        random = Random()
        randomWikiLinks = []
        numberOfPages = 2

        while True:
            randomWikiName = random.choice(wikiNames)
            if not randomWikiName in randomWikiLinks:
                url = requests.get(f"https://pt.wikipedia.org/wiki/{randomWikiName}").url
                randomWikiLinks.append(url)
                numberOfPages -= 1
            if numberOfPages == 0:
                break
        
        print(randomWikiLinks)
        await ctx.send(f'Boa sorte {reaction(*args)} \n\nIniciar em: {randomWikiLinks[0]} \nChegar em: {randomWikiLinks[1]}')
        await ctx.send('- Se quiser saber as regras só mandar um _Regras. \n- COMEÇAR pra iniciar, ou CANCELAR (bem autoexplicativo).')
        finalMessage = ""

        while (True):
            confirmation_msg = await self.client.wait_for('message')
            if (confirmation_msg.content == "COMEÇAR"):
                break
            elif (confirmation_msg.content == "CANCELAR"):
                await ctx.send(f"Já? {reaction('krl')} \n- Jogo Cancelado")

                self.isRunning = False
                return

        counter_msg = await ctx.send("'")
        for i in range(3, 0, -1):
            await counter_msg.edit(content=f"{'-'*10} {i} {'-'*10}")
            sleep(1)
        await counter_msg.edit(content=f"{'-'*5} COMEÇO {'-'*5}")
        
        players = []
        startingTime = time()['hora']
        while True:
            msg = await self.client.wait_for('message')
            
            content = msg.content
            print(content)

            if content == "FOI":
                not_converted_end_time = time()['hora']
                end_time = datetime.strptime(not_converted_end_time, TIME_FORMAT) 
                initial_time = datetime.strptime(startingTime, TIME_FORMAT)
                individualEndTime = end_time - initial_time
                
                players.append((individualEndTime, msg.author))
                print(players)

                await ctx.send(f"<@!{players[-1][1].id}> CABO <:PogChamp:797648070606716939> \nComeçou em: {startingTime} \nTerminou em: {not_converted_end_time}\n\n Isso são {players[-1][0]}!")
            elif content == "ACABOU":

                print(players)
                finalMessage += f"{'-'*10} SCORE {'-'*10}\n"
                players.sort()
                
                i = 1
                for player in players:
                    finalMessage += f"{i}° Lugar: <@!{player[1].id}> - {player[0]}\n"
                    i += 1
                break
            elif content == "_Regras":
                await ctx.send('''Tem que ir do primeiro link da wiki até o segundo só usando os links azuis.
Isso é uma competição, eu vo marca as pontuações. Se vc tá jogando sozinho, bom... isso é triste <:LULW:647892916185858088>
Escreve FOI quando conseguir, e escreve ACABOU quando quiser ver quem ganhou''')

        print(players)
        
        await ctx.send(finalMessage)
        self.isRunning = False


def setup(client):
  client.add_cog(Wiki(client))