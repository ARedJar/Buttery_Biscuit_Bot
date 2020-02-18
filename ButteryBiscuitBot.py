"""
Buttery Biscuit Bot!

Chat reply basics: https://pythonprogramming.net/discordpy-basic-bot-tutorial-introduction/
More in depth guide: https://realpython.com/how-to-make-a-discord-bot-python/
Every audio guide I found had various non-working function calls, so I had to build that mostly just by reading the api. Let me know if you have questions, but the code block should be pretty easy to copy for new mp3's.

API: https://discordpy.readthedocs.io/en/latest/api.html
Bot API: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
^Note that the bot is a subclass of client, so can do anything that the client can (just switch client.whatever to bot.whatever)

In general, any api functions that are a 'coroutine' will need an 'await' or they'll probably get skipped on execution as the next block of code will just go ahead and run.

See README.txt for necessary libraries etc...

To run - navigate to bot's directory in cmd, then enter:
python ButteryBiscuitBot.py
Or for the server:
python3.8 ButteryBiscuitBot.py
"""

import os

import discord
from discord.ext import commands

import asyncio                                                              # Needed for coroutine / await functionality, which discord.py is built around.

from dotenv import load_dotenv

#Initialize Bot
load_dotenv()
token = os.getenv('DISCORD_TOKEN')                                          # Storing the token in a separate env file that won't be on GitHub - for security.
bot = commands.Bot(command_prefix = "!")


#Print a message to console to verify that bot is activated / connected to discord.
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


#Activates on chat messages; should be a switch but python doesn't support them so it'd have to be like a dictionary, which may be tricky to implement with 'hell' (for which I'd like to retain the ability to work anywhere in the message)
#Can also consider a function for a user prompt like 'when I say <arg1> you say <arg2>'
@bot.event
async def on_message(message):
    if message.author == bot.user:                         # Prevent the bot from replying to itself ad-infinitum, in case we ever create a recursive reply.
        return
    
    for key in callResponseDict:
        if key in message.content.lower():
            resp = callResponseDict[key]
            await message.channel.send(resp)

    # This is necessary to allow bot commands to come through (such as music), since we have overwritten the default on_message event handling https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working
    await bot.process_commands(message)

callResponseDict = {
    'hell': 'Yeah Dog!',
    'uwu': 'Hewwwwoo~~',
    'bb': 'BOBBBBBYYYYYYY',
    'bee': 'BEE-THEMED STRIPPERS!!',
    'kiddy': 'hey there ya dingus'
}

#------------------------------Mp3 command zone!-----------------------------

#Washington
@bot.command(
    name = 'washington',
    aliases = ['Washington'],
    description = 'He\'s Coming!',
    pass_context = True,
)
async def washington(context):
    await playMP3(beautifulSongsDict['washington'], validChannelNames, context)

#ButteryBiscuitBase
@bot.command(
    name = 'biscuit',
    aliases = ['Biscuit'],
    description = 'All your base...',
    pass_context = True,
)
async def biscuit(context):
    await playMP3(beautifulSongsDict['biscuit'], validChannelNames, context)

async def playMP3(mp3FilePath, channelNames, context):
    # Only play music if user is in a voice channel
    if await isUserInChannel(context, channelNames):
        # Connect to voice chat and play .mp3
        voice_channel = await getCurrentVoiceChannelInstance(context)
        vc = await voice_channel.connect()                                                                       #Returns an object of the voice channel that it has connected to.
        vc.play(discord.FFmpegPCMAudio(mp3FilePath), after = lambda e: print('done', e))    #Can add error handling to the 'after' portion.. I believe..
        # Wait for music to finish
        while vc.is_playing():
            await asyncio.sleep(1)
        # Disconnect after music stops
        vc.stop()
        await vc.disconnect()
    else:
        await context.message.channel.send('User is not in a voice channel.')

async def isUserInChannel(context, channelNames):
    # Grab the user who sent the command and the voice channel they are in
    voice_channel = await getCurrentVoiceChannelInstance(context)
    if voice_channel != None and voice_channel.name in channelNames:
        return True
    else:
        return False

async def getCurrentVoiceChannelInstance(context):
    user = context.message.author
    voice_channel = user.voice.channel
    return voice_channel

beautifulSongsDict = {
    'biscuit': './Music/ButteryBiscuitBase.mp3',
    'washington': './Music/Washington.mp3'
}

validChannelNames = [
    'Bobby Lobby',
    'General'
]

#-----------------------------Actually run the bot----------------------------
bot.run(token)


#TODO:
    #Add uwu-translator function
    #Mess w/ Bobby somehow
    #Rename washington to 'he's coming'? Has punctuation and a space so probably horrible, but I want it to be invokable that way >.>
    #Add songs or other commands, build out additional functionality