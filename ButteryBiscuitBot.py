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

    if 'hell' in message.content.lower():                  # Works anywhere in the string (.lower) :D
        await message.channel.send('Yeah Dog!')
    elif message.content == 'uwu':                         # I kinda want to make this a function instead to 'uwu'-ize a message...
        await message.channel.send('Hewwwwoo~~')
    elif message.content == 'bb':                          # Surely we can come up with something more annoying, maybe it can do something when he logs in? :D
        await message.channel.send('BOBBBBBYYYYYYY')
        
    await bot.process_commands(message)                    # This is necessary to allow bot commands to come through (such as music), since we have overwritten the default on_message event handling https://stackoverflow.com/questions/49331096/why-does-on-message-stop-commands-from-working

#------------------------------Mp3 command zone!-----------------------------

#Washington
@bot.command(
    name = 'washington',
    aliases = ['Washington'],
    description = 'He\'s Coming!',
    pass_context = True,
)
async def washington(context):
    # Grab the user who sent the command and the voice channel they are in
    user = context.message.author
    voice_channel = user.voice.channel
    # Only play music if user is in a voice channel
    if voice_channel != None and voice_channel.name != 'AFK':
        # Connect to voice chat and play .mp3
        vc = await voice_channel.connect()                                                               #Returns an object of the voice channel that it has connected to.
        vc.play(discord.FFmpegPCMAudio('./Music/Washington.mp3'), after = lambda e: print('done', e))    #Can add error handling to the 'after' portion.. I believe..
        # Wait for music to finish
        while vc.is_playing():
            await asyncio.sleep(1)
        # Disconnect after music stops
        vc.stop()
        await vc.disconnect()
    else:
        await context.message.channel.send('User is not in a voice channel.')

#ButteryBiscuitBase
@bot.command(
    name = 'biscuit',
    aliases = ['Biscuit'],
    description = 'All your base...',
    pass_context = True,
)
async def biscuit(context):
    # Grab the user who sent the command and the voice channel they are in
    user = context.message.author
    voice_channel = user.voice.channel
    # Only play music if user is in a voice channel
    if voice_channel != None and voice_channel.name != 'AFK':
        # Connect to voice chat and play .mp3
        vc = await voice_channel.connect()                                                                       #Returns an object of the voice channel that it has connected to.
        vc.play(discord.FFmpegPCMAudio('./Music/ButteryBiscuitBase.mp3'), after = lambda e: print('done', e))    #Can add error handling to the 'after' portion.. I believe..
        # Wait for music to finish
        while vc.is_playing():
            await asyncio.sleep(1)
        # Disconnect after music stops
        vc.stop()
        await vc.disconnect()
    else:
        await context.message.channel.send('User is not in a voice channel.')


#-----------------------------Actually run the bot----------------------------
bot.run(token)


#TODO:
    #Get some sort of switch implementated for the on_message commands, rather than current if / elif block (probably needs to be a dictionary, python doesn't support switch / catch blocks).
    #Add uwu-translator function
    #Mess w/ Bobby somehow
    #Rename washington to 'he's coming'? Has punctuation and a space so probably horrible, but I want it to be invokable that way >.>
    #Add songs or other commands, build out additional functionality