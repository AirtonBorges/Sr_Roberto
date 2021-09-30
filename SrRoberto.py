
from utils import *

SrRobertoKey = os.getenv('SR_ROBERTO_API_KEY')
BOT_CHAT_ID = 716395800791613512
TIME_FORMAT = "%H:%M:%S"
client = commands.Bot(command_prefix=['<:strawHat_Pepe:632411513990152223> ', '<:strawHat_Pepe:632411513990152223>'])

@client.event
async def on_ready():
    print(f"Awo {client.user}")


def search(pergunta, getLink=False): # Scrapes Branly to find (homework) answers
    source = ""
    resposta = ""
    answerLink = ""

    # Get the source of the page, will only work if the question is a link
    try:  
        source = requests.get( pergunta ).text
        print("It's a link")
    
    except Exception as e:
        # If's not a link, then its a phrase
        print(e)
        
        # Put the phase in the query url
        responseLink = f"https://brainly.com.br/app/ask?entry=hero&q={ pergunta }"
        
        # Use Selenium to get the dinamicaly generated page
        driver = Driver()
        source = driver.getPage(responseLink)

        # Get a nice soup
        soup = BeautifulSoup(source, "lxml")

        # Find the first quesion
        answerbox = soup.find("div", {"class": "js-page-wrapper"})
        firstAnswerWrapper = answerbox.find("div", {"data-testid": "search-item-facade-wrapper"})
        
        # Get the href of the first question, and put it in the full link
        answerId = firstAnswerWrapper.find(href=True)['href']
        answerLink = f"https://brainly.com.br{ answerId }"
        
        # Get the source of the first answer
        source = requests.get( answerLink ).text

    # Get the soup of the answer
    soup = BeautifulSoup(source, "lxml")
    
    # Find the answer component
    answerBox = soup.find('div', {"data-test": "answer-box-text"})

    # Get the answer text, and put a new line where a component id
    # I'll have to format the text a little bit better sometime in the future
    resposta = answerBox.get_text("\n")
    
    # Remove unecessary links, if they exist
    try:
        resposta = resposta[:resposta.index("Veja mais")]
    except Exception as e:
        print("Não tinha veja mais")
    
    link = f"Link: {answerLink}"
    resposta = f"{resposta}{link if getLink else ''}"
    print(resposta)

    # return the answer
    return resposta

class Number: # store a simple number
    num = 2  
    num *= 2
    if num >= 2000:
        num = randint(1, 20)


class Opa:
    get = [f'{"o" * o}pa' for o in range(2, 100)]


class SpeedRun:
    isRunning = False


# @client.command(aliases=Opa.get)
# async def opa(ctx, *args):
#     # uses an list of opa to make so the user can use a lot of o's
#     le = time()['letra']
#     pa = time()['periodo']

#     # if the number of letters is more than 2000, the bot just pics a new random number of letters to display

#     # multiply a [letra] of the [periodo] by that random number to make it look like is an old person answering
#     pl = pa.split(le, 1)
#     pl.insert(1, le * Number.num)
#     pl = ''.join(pl)

#     await ctx.send(f"{pl} {reaction(*args)}")      


# @client.command(aliases=['Horas', 'QueHorasSão'])
# async def hora(ctx, *args):
#     # answers with the time
#     await ctx.send(f'São {time()["hora"]} {reaction(*args)}')
#     time()

     
@client.command(aliases=['brainly', 'Brainly', 'Responda,', 'Responda:', 'responda,', 'responda:'])
async def resposta(ctx, *args):
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
    message = search(text, getLink)
    print('RESPOSTA: ', message)

    # Send the answer 
    await ctx.send(f'<:Thonk:633762138040565798>... {message}')
    

@client.command(aliaes=["WikiSpeedrun"])
async def wikispeedrun(ctx, *args):
    if SpeedRun.isRunning:
        await ctx.send("Já tem uma speedRun acontecendo, acaba primeiro antes de ir pra outra <:RAGEY:662481054719803443>")
    else:
        SpeedRun.isRunning = True

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
            confirmation_msg = await client.wait_for('message')
            if (confirmation_msg.content == "COMEÇAR"):
                break
            elif (confirmation_msg.content == "CANCELAR"):
                await ctx.send(f"Já? {reaction('krl')} \n- Jogo Cancelado")

                SpeedRun.isRunning = False
                return

        counter_msg = await ctx.send("'")
        for i in range(3, 0, -1):
            await counter_msg.edit(content=f"{'-'*10} {i} {'-'*10}")
            sleep(1)
        await counter_msg.edit(content=f"{'-'*5} COMEÇO {'-'*5}")
        
        players = []
        startingTime = time()['hora']
        while True:
            msg = await client.wait_for('message')
            
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
        SpeedRun.isRunning = False


@client.command()
async def aleatório(ctx, *args):
    getRandomPageUrl = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"
    randomPage =  requests.get(getRandomPageUrl).url
    
    await ctx.send(f"Aqui o sua página aleatória {reaction(*args)}\n\nLink:{randomPage}")


client.run(SrRobertoKey)
