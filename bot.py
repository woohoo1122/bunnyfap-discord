import discord
import random
from thumbs import getImage, getLinks, getVid
from key import token # you need your own bot token

ffmepg = r'C:\ffmpeg\bin\ffmpeg.exe'

# vv Token, in case I fuck  up the variable vv


print('Wait 5 seconds for the bot to initialize...')
client = discord.Client()
global vc
global connected

# manually spliced because i am a godly human neural network
prelink = 'https://bunnyfap.com/tags/'
tag = 'eye-contact'

links = getLinks(prelink + tag)

reactions = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':ten:']

@client.event
async def on_message(message):
    
    global links
    global tag
    
    # print('found')
    # print(message.content.split(' '))
    # what str.find() does is return -1 if it doesnt exist
     # Change Tag
    try:
        if message.content.split(' ')[1] == 'tag'and message.content.find('~porn') != -1:
            tag = message.content.split(' ')[2]
            await message.channel.send('Changing link to: ' + prelink + tag + '\n\nPlease be patient while our hamster loads your page')
            links = getLinks(prelink + tag)
            await message.channel.send('Loaded the page. Test Image:')
    except:
        if len(message.content.split(' ')) == 2 and message.content.find('~porn') != -1:
            await message.channel.send('Current tag is: ' + tag)

    if message.content.find('~porn') != -1:
        if message.content.find('v') != -1:
            getVid(links)
            await message.channel.send(file=discord.File('temp.mp4'))
        else:
            getImage(links)
            await message.channel.send(file=discord.File('temp.jpg'))
    try:
        if message.attachments[0].url.find('.jpg') or message.attachments[0].url.find('.png'):
            for r in reactions:
                await message.add_reaction(r)
       
    except:
        pass


client.run(token)
