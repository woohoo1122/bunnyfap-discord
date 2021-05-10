# so many imports so sorry if anyone actually wants to use this
import re
import shutil
import requests
import random
import urllib
import subprocess
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen

# 
def getLinks(URL):
    #----------------------------------OPTIONS-------------------------------------
    # i got this from stack overflow but i cant remmeber the link!
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.    --> this was from stackoverflow
    options.add_argument('log-level=3') # disables verbose logging in terminal
    options.add_argument('--start-maximized') # to load more links faster
    browser = webdriver.Chrome(chrome_options=options) # start the browser session
    #----------------------------------LOAD PAGE-------------------------------------
    links = [] # the goal is to scrape the web to feed clean links into this list
    browser.get(URL) # this sends the browser to the link\
    sleep(3) # this makes it force wait because sometimes some images load faster and the script jumps the gun. Test it out for yourself!
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'v-image__image--cover')) # i got this implementation from stack overflow, and i like it
    WebDriverWait(browser, 5).until(element_present) # wating


    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    # #----------------------------------INFINITE SCROLL SCRIPT-------------------------------------
    # THIS IS LITERALLY COPY PASTED CODE. IF THIS IS ILLEGAL PLS MESSAGE ME, THANK YOU
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    for i in range(6):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(0.3)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height: # why do i even need this? isn't this reduntant for an infinite scroll script? 
            break
        last_height = new_height

    #----------------------------------GET ALL LINKS IN PAGE-------------------------------------

    soup = bs(browser.page_source, 'html.parser') # after all the special selenium browser preprocessing, i can finally scrape the raw javescript loaded html
    bitches = soup.find_all('div', class_='v-image__image--cover') # bring on the image links by finding the html divider with this specific class name. for other sites, fine tune this 

    # scrub for links
    for bitch in bitches:
        # print(bitch['style'])
        if bitch['style'].find('url') != -1: # this is specifc html shit you just gotta alter this line to intuition. i cant figure out how to automate this. 
            link = re.search("(?P<url>https?://[^\s]+)", bitch['style']).group("url") # copy pasted from stackoverflow, forgot the link. it brute forces scrubbing the link instead of html formatting bs
            linka = link[:-3] # there's some weird bug where if i append link[:-3] to links nothing happens
            links.append(linka) # and we're done! we sent it all to links. now with our raw links, we have to find a way to download it. 
    return links # when i hooked this to my bot, i had to make this a function that returns links, which i send back to the download function later. it used to be a good ol' recipe program. 

#------------------------------DEBUG------------------------------
# print(links)
# for i in links:
#     print(i)
#------------------------------DEBUG END------------------------------

# browser.close()

#------------------------------DOWNLOAD ONE IMAGE------------------------------
def getImage(links):
    shawty = random.choice(links)
    print(shawty)

    # This makes imgur thumbs larger
    if shawty.find('imgur') != -1:
        # print('OLD LINK:', shawty)
        shawty = shawty[:-5] + shawty[-4:]

    try:
        urlretrieve(shawty, 'temp.jpg')

    except urllib.error.HTTPError:
        r = requests.get(shawty, stream=True)
        with open("temp.jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def getVid(links):
    shawty = random.choice(links)
    

    # This IS NECESSARY FOR VIDEOS OR ELSE IT DOESNT WORK
    if shawty.find('imgur') != -1:
        # print('OLD LINK:', shawty)
        shawty = shawty[:-5] + shawty[-4:]

    # PREPROCESSING TO CONVERT LINKS TO VIDEOS
    if shawty.find('poster') != -1:
        shawty = shawty[:-11] + '.mp4'
    else:
        shawty = shawty[:-4] + '.mp4'

    print(shawty)

    try:
        urlretrieve(shawty, 'temp.mp4')

    except urllib.error.HTTPError:
        r = requests.get(shawty, stream=True)
        with open("temp.mp4", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    
    # result = subprocess.run('ffmpeg -i temp.mp4 -b:a 800k temp.mp4 -y')
    # print(result)


# -----------------------THIS IS FOR BATCH DOWNLOADS--------------------------------------
'''for i, bitch in enumerate(links):
    print(bitch)

    try:
        urlretrieve(bitch, str(i)+ '.jpg')
    except urllib.error.HTTPError:
        # req = Request('https://bunnyfap.com/tags/eye-contact', headers={'User-Agent': 'Mozilla/5.0'})
        # webpage = urlopen(req).read()
        # urlretrieve(bitch, str(i)+ '.jpg')
        r = requests.get(bitch, stream=True)
        with open(str(i) + ".png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
'''
# browser.close()