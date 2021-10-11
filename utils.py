from typing import Text
import discord
from time import strftime, sleep
from datetime import datetime
from random import Random, randint, random
from discord import message
from discord import flags
from discord.ext import commands
from bs4 import BeautifulSoup
from discord.message import Message
import requests
from requests.api import get, put
from selenium import webdriver
import os
import csv

SrRobertoKey = os.getenv('SR_ROBERTO_API_KEY')
BOT_CHAT_ID = 716395800791613512
TIME_FORMAT = "%H:%M:%S"
client = commands.Bot(command_prefix=['<:strawHat_Pepe:632411513990152223> ', '<:strawHat_Pepe:632411513990152223>'])


def reaction(*args):  # Returns a reaction depending on the words the user... uses
    mean_words = ('cu', 'veio', 'puta', 'caralho', 'fdp', 'krl', 'crl', 'karalho')
    emote = "<:strawHat_Pepe:632411513990152223>"

    for word in args:
        print("Args: ", args)
        if word in mean_words:
            emote = "<:wtf:672114773252636682>"
    return emote


# Get a dict with the programs to open or close on the csv file
def get_dict(csv_name, get_path=False):
    with open(csv_name, 'r', encoding='utf-8') as csv_file:
        processes = csv.reader(csv_file)

        v_dict = {}
        
        for row in processes:
            if get_path:
                v_dict.update({row[0]: row[2]})
            else:
                v_dict.update({row[0]: row[1]})

        return v_dict


def time():  # returns a dict with the current time and the period of the day
    tinfo = {'hora': strftime(TIME_FORMAT), 'periodo': 'No', 'letra': 'a'}

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

    def getUrl(self, execute):
        with self.driver as browser: 
            # Get a link, then wait a bit for it to load
            browser.get(execute)
            
            browser.current_url

            sleep(3)

            return browser.page_source

class Wikis:
    def __init__(self):
        self.wikis = get_dict("ListOfWikis.csv")
    def getNames(self):
        names = []
        
        for k in self.wikis.keys():
            names.append(k)

        return names


def search_on_brainly(pergunta, getLink=False): # Scrapes Branly to find (homework) answers
    source = ""
    resposta = ""
    answerLink = ""

    # Get the source of the page, will only work if the question is a link
    try:  
        source = requests.get( pergunta ).text
        print("It's a link")
    
    except Exception as e:
        return "Por enquanto sou meio burro, favor fornecer o link da pergunta"
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
        firstAnswerWrapper = answerbox.findseum("div", {"data-testid": "search-item-facade-wrapper"})
        
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
