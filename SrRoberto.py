from typing import Text
import discord
from time import strftime, sleep
from random import randint
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os

SrRobertoKey = os.getenv('SR_ROBERTO_API_KEY')
print(SrRobertoKey)

client = commands.Bot(command_prefix=['<:strawHat_Pepe:632411513990152223> ', '<:strawHat_Pepe:632411513990152223>'])

@client.event
async def on_ready():
    print(f"Awo {client.user}")

def reaction(*args):  # Returns a reaction depending on the words the user... uses
    mean_words = ('cu', 'veio', 'puta', 'caralho', 'fdp', 'krl', 'crl', 'karalho')
    emote = "<:strawHat_Pepe:632411513990152223>"

    for word in args:
        print("Args: ", args)
        if word in mean_words:
            emote = "<:wtf:672114773252636682>"
    return emote


def time():  # returns a dict with the current time and the period of the day
    tinfo = {'hora': strftime('%H:%M'), 'periodo': 'No', 'letra': 'a'}

    if int(tinfo['hora'][:2]) <= 5:  # from 00 am to 5 am
        tinfo['periodo'] = 'Madrugada'
        pass
    elif int(tinfo['hora'][:2]) <= 11:  # from 6 am to 11 am
        tinfo['periodo'] = 'dia'
        tinfo['letra'] = 'i'
        pass
    elif 18 >= int(int(tinfo['hora'][:2])):  # from 12 am to 6 pm
        tinfo['periodo'] = 'Tarde'
        pass
    elif 23 >= int(tinfo['hora'][:2]):  # from 6 pm to 11 pm
        tinfo['periodo'] = 'Noite'
        tinfo['letra'] = 'o'
        pass

    print('-' + tinfo['hora'], tinfo['periodo'])
    return tinfo

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


class Driver: # Selenium functionality 
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless') # Make the driver invisible
        options.add_argument("disable-gpu")

        self.driver = webdriver.Chrome('chromedriver', options=options)
    def getPage(self, link):
        with self.driver as browser: 
            # Get a link, then wait a bit for it to load
            browser.get(link)
            sleep(3)

            return browser.page_source


@client.command(aliases=Opa.get)
async def opa(ctx, *args):
    # uses an list of opa to make so the user can use a lot of o's
    le = time()['letra']
    pa = time()['periodo']

    # if the number of letters is more than 2000, the bot just pics a new random number of letters to display

    # multiply a [letra] of the [periodo] by that random number to make it look like is an old person answering
    pl = pa.split(le, 1)
    pl.insert(1, le * Number.num)
    pl = ''.join(pl)

    await ctx.send(f"{pl} {reaction(*args)}")      


@client.command(aliases=['Horas', 'QueHorasSão'])
async def hora(ctx, *args):
    # answers with the time
    await ctx.send(f'São {time()["hora"]} {reaction(*args)}')
    time()


@client.command(aliases=['brainly', 'Brainly', 'Responda,', 'Responda:', 'responda,', 'responda:'])
async def resposta(ctx, *args):
    await ctx.send(f'Pera já vejo', tts=True)

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
    await ctx.send(f'<:Thonk:633762138040565798>... {message}', tts=True)

client.run(SrRobertoKey)
