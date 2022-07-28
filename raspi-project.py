#!/usr/bin/env python3
#import -c !/usr/bin/env python3

# from sense_hat import SenseHat
from time import sleep
import time
import requests
import speech_recognition as sr
import re
from playsound import playsound
from gtts import gTTS
from datetime import datetime
import os 
import pyjokes
import wikipedia
import webbrowser
from PIL import Image
import pyautogui
from time import localtime
from requests import get
from urllib.parse import quote
from bs4 import BeautifulSoup
from random import randint
from json import loads
import json
from playwright.sync_api import sync_playwright # pip install playwright, playwright install, Chromium sur la maachine


def textToAudioFile(str, filename):
    """"
    This function convert type string to an MP3 file. 
    If the file already exists, he is removed, then he is created in the current repository.
    Don't forget to add the .mp3 extension in the filename you give.
    You can now call playsound like : playsound(os.getcwd() + "\\filename")
    """
    path = os.getcwd()
    if os.path.exists(path + filename): 
        os.remove(path + filename)    
    myobj = gTTS(text=str, lang='en', slow=False)
    myobj.save("audio/" + filename)



def get_dynamic_soup(url: str) -> BeautifulSoup:
    """
    Can't get the contents of a dynamic website like youtube using requests package.
    We need first to get to the url, then render the response using something like chromium in the background,
    then pass the results to beautiful soup to get a formatted list in HTML.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch()

        # Open a new browser page
        page = browser.new_page()

        # Open our test file in the opened page
        page.goto(url)

        # Process extracted content with BeautifulSoup
        soup = BeautifulSoup(page.content(), "html.parser")

        browser.close()

        return soup  # return formatted list in HTML



def get_info(lt):
    """
    Get inside the main more informations from the microphone
    """       
    try:
        with sr.Microphone() as source:
            voice = r.listen(source,phrase_time_limit=lt)
            info = r.recognize_google(voice)
            print(info)
            return info
    except:
        print("Error !")
        pass



# get audio from the microphone
r = sr.Recognizer()
word = ""

dict = {'me':'lilian.andres@etu.univ-lyon1.fr','lilian':'andres.universite@gmail.com','dylan':'dylan.leclercq@etu.univ-lyon1.fr'}

print("Starting...")

while not "stop" in word:

    with sr.Microphone() as source:
        audio = r.listen(source)    
    
    try:
        print("\nHow can I help you ? ")
        word = r.recognize_google(audio)
        print(word)
    except:
        playsound(os.getcwd() + "\\audio\\error.mp3")
        continue

    hourAsk = re.compile("time")
    jokeAsk = re.compile("joke")
    wikiAsk = re.compile("Wikipedia")
    newsAsk = re.compile("latest new")
    screenAsk = re.compile("screenshot")
    youtubeAsk = re.compile("YouTube") 
    coinAsk = re.compile("coin")
    weatherAsk = re.compile("weather")
    mailAsk = re.compile("mail")
    yesAnswer = re.compile("yes")

    if hourAsk.search(word):
        """
        [* time *]
        """
        now = datetime.now()
        current_time = now.strftime("%H:%M %p")
        mytext = "It is " + current_time     
        textToAudioFile(mytext, "audio.mp3")                                      
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        print(mytext)


    elif jokeAsk.search(word):
        """
        [* joke *]
        """

        joke = pyjokes.get_joke(language="en", category="all")
        textToAudioFile(joke, "audio.mp3")                                      
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")


    elif wikiAsk.search(word):
        """
        [Your search] + Wikipedia
        """

        word.replace("Wikipedia", "")
        results = wikipedia.summary(word, sentences=3)
        textToAudioFile("According to Wikipedia", "audio.mp3")                                      
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        print(results)
        textToAudioFile(results, "audio.mp3")                                      
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")


    elif newsAsk.search(word):
        """
        [* latest news *]
        """

        news = webbrowser.open_new_tab("https://www.lemonde.fr/")
        newsannouce = 'Here are some headlines from Le Monde, Happy reading'
        textToAudioFile(newsannouce, "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
    

    elif screenAsk.search(word):
        """
        [* screenshot *]
        """

        year = str(localtime().tm_year)
        month = str(localtime().tm_mon)
        day = str(localtime().tm_mday)
        hour = str(localtime().tm_hour)
        minute = str(localtime().tm_min)
        second = str(localtime().tm_sec)
        Date = "{}{}{}{}{}{}.png".format(year, month, day, hour, minute, second)
        User = os.getlogin()
        SavePath = r"D:\Users\{}\Pictures".format(User)
        pyautogui.screenshot(os.path.join(SavePath, Date))
        im = Image.open(os.path.join(SavePath, Date))
        im.show()


    elif youtubeAsk.search(word):
        """
        [Your search] + on Youtube
        """

        searchTerm = word.split()
        _url = "https://www.youtube.com/results?search_query=" + quote(" ".join(searchTerm[:-2]))
        soup = get_dynamic_soup(_url)
        videos = soup.findAll('a', attrs={
            "class": "yt-simple-endpoint style-scope ytd-video-renderer"
        })[1:4]
        # [1:4] instead of [:3] to dodge Youtube ads video
        ytbannouce = "I found many videos. Here are the first links, enjoy !"
        textToAudioFile(ytbannouce, "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        names = list()
        links = list()
        for i in range(len(videos)):
            names.insert(i, videos[i]["title"])
            links.insert(i, "https://www.youtube.com" + videos[i]["href"])
        print("\nResults list :")
        for i in range (3):            
            print("\n" + str(i+1) + " - " + names[i] + " : " + links[i])
        
        textToAudioFile("Should I open the first video I found ?", "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        confirmation = get_info(5)
        time.sleep(0.5)
        if yesAnswer.search(confirmation):        
            webbrowser.open_new_tab(links[1])    

        
    elif coinAsk.search(word):
        """
        [* coin *]
        """

        if randint(1, 2) == 1:
            coin = "It landed on heads !"
        else:
            coin = "It landed on tails !"
        textToAudioFile(coin, "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")


    elif weatherAsk.search(word):
        """
        [* weather *]
        """

        response = get("http://ipinfo.io/json")   # get city name from IP address
        responseDecode = loads(response.text)
        city = responseDecode["city"]
        api_key = os.getenv('API_KEY')
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        url = base_url + "q=" + city + "&appid=" + api_key   
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            temperature = main['temp']
            temperatureDeg = float(temperature)
            celsius = round(temperature - 273.15)  # kelvin to Celsius
            celsius = str(celsius)
            # getting the humidity
            humidity = main['humidity']
            humidity = str(humidity)
            # getting the pressure
            pressure = main['pressure']
            # weather report
            report = data['weather']
            print(f"{city:-^30}")
            print(f"Temperature: {celsius}°C")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure}")
            print(f"Weather Report: {report[0]['description']}")
            weather = "The temperature is " + celsius + " degrees. The humidity is " + humidity + " %, and the weather report is : " + report[0]['description']
            textToAudioFile(weather, "audio.mp3")
            playsound(os.getcwd() + "\\audio\\audio.mp3")
            os.remove(os.getcwd() + "\\audio\\audio.mp3")
        else:
            # showing the error message
            print("Error in the HTTP request")
        
    
    
    elif mailAsk.search(word): 
        """
        mail to + [your contact name] / send a mail to + [your contact name] 
        """ 

        name = word.split()
        name = name[name.index('to') + 1]  # get the name
        name = name.lower()     

        #ask for the subject
        textToAudioFile("What is the subject ?", "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        subject = get_info(5)
        time.sleep(0.5)

        #ask for the message
        textToAudioFile("What is the message ?", "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        msg = get_info(10)
        time.sleep(0.5)

        #ask for a confirmation before sending
        text = f"Okay, can I send the mail to {dict[name]} ?"
        textToAudioFile(text, "audio.mp3")
        playsound(os.getcwd() + "\\audio\\audio.mp3")
        os.remove(os.getcwd() + "\\audio\\audio.mp3")
        confirmation = get_info(5)
        time.sleep(0.5)
        if yesAnswer.search(confirmation): 
            #send the mail 
            response = requests.get(f"http://sea-president.ovh/english-project-lilian?to={dict[name]}&subject={subject}&message={msg}&headers=From:{dict['me']}")
            textToAudioFile("Email sent with success", "audio.mp3")
            playsound(os.getcwd() + "\\audio\\audio.mp3")
            os.remove(os.getcwd() + "\\audio\\audio.mp3")

#sense.clear()