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
from dotenv import load_dotenv

import asyncio                                                              # Needed for coroutine / await functionality, which discord.py is built around.
from datetime import datetime, date, time                                   # Date and time function, for some prelim console logging I'm planning on doing -Jon

#Initialize Bot
load_dotenv()
token = os.getenv('DISCORD_TOKEN')                                          # Storing the token in a separate env file that won't be on GitHub - for security.
bot = commands.Bot(command_prefix = "!")

vnumber = '0.0.1.8 alpha'
    # this is the top version number, only thing that needs to be updated for !version to be up to date
    # please edit this anytime an update is made!
pnotes = vnumber + '\n added version and patch notes commands \n !version will now print the current version number (note this needs to be changed manually in the code) \n !patchnotes will now print the current patch notes (also need to be changed manually) \n Added proper error handling for if user calls bot but is not in a voicechannel \n Working on implementing timestamping for logging purposes\n Working on adding shortbiscuit command to play snippet of biscuit \n Can now display images in chat, currently only !chrispenis and !biscuitfaces work'
    # same as vnumber this is where the text for patch notes goes, please update this (also don't let it get too long maybe only the most recent build?)

"""
Print a message to console to verify that bot is activated / connected to discord.
"""
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

"""
For a set of given messages, the bot responds with pre-defined responses in the "callResponseDict"

Parameters
----------
first : string
    The message any given user has typed into any text channel this bot can access

Returns
-------
string
    The appropriate response for a given "call" from a message

Raises
------
Does Not Error
"""
@bot.event
async def on_message(message):
    # TODO mdman2014 2/23/2020 - check that the author it either a quaid or a duckling, no outsiders
    if message.author == bot.user:                         # Prevent the bot from replying to itself ad-infinitum, in case we ever create a recursive reply.
        return
    
    standardizedMessage = message.content.lower()

    for key in callResponseDict:
        if key in standardizedMessage:
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


"""
Allows the user to tell what version is currently running

Parameters
----------
first : Context
    The context of the text channel in which the command was raised

Returns
-------
string
    The version of the bot and timestamp of the call

Raises
------
Does Not Error
"""
@bot.command(
    name = 'version',
    aliases = ['Version'],
    description = '',
    pass_context = True,
)
async def version(ctx):
    await ctx.message.channel.send(vnumber)
    currentTimestamp = datetime.now()
    currentTimestamp_string = currentTimestamp.strftime("%d/%m/%Y %H:%M:%S")
    await ctx.message.channel.send(currentTimestamp_string)

"""
Allows the user to retrieve the updated patch notes

Parameters
----------
first : Context
    The context of the text channel in which the command was raised

Returns
-------
string
    The patchnotes for the most recent release

Raises
------
Does Not Error
"""   
@bot.command(
    name = 'patchnotes',
    aliases = ['Patchnotes', 'PatchNotes'],
    description = 'what does this do',
    pass_context = True,
)
async def patchnotes(ctx):
    await ctx.message.channel.send(pnotes)

#------------------------------Picture Zone!-----------------------------

"""
ChrisPenis
"""
@bot.command(
    name = 'chrispenis',
    aliases = ['ChrisPenis', 'Chrispenis'],
    description = 'Cool wafers to desired...',
    pass_context = True,
)
async def chrispenis(channel):
    await channel.send(file=discord.File('/ButteryBiscuitBot/pythbot/pictures/chrispenis.jpg'))
    # this sends the file directly to discord, there is a way to do so with filelike objects (dunno what those are) but I couldn't get it to work
    
"""
biscuitfaces
"""
@bot.command(
    name = 'biscuitface',
    aliases = ['biscuitfaces', 'BiscuitFace', 'BiscuitFaces'],
    description = 'They are buttery...',
    pass_context = True,
)
async def biscuitface(channel):
    await channel.send(file=discord.File('/ButteryBiscuitBot/pythbot/pictures/biscuitface.jpg'))
    
"""
pepperoni
"""
@bot.command(
    name = 'pepperoni',
    aliases = ['Pepperoni', 'heyyotony', 'freshpepperoni', 'cleverthoughts', 'CleverThoughts'],
    description = 'Hey yo tony, whered you get that fresh pepperoni',
    pass_context = True,
)
async def pepperoni(channel):
    await channel.send(file=discord.File('/ButteryBiscuitBot/pythbot/pictures/pepperoni.png'))


#------------------------------Mp3 command zone!-----------------------------

"""
Washington
"""
@bot.command(
    name = 'washington',
    aliases = ['Washington'],
    description = 'He\'s Coming!',
    pass_context = True,
)
async def washington(context):
    await playMP3(beautifulSongsDict['washington'], validChannelNames, context)

"""
ButteryBiscuitBase
"""
@bot.command(
    name = 'biscuit',
    aliases = ['Biscuit'],
    description = 'All your base...',
    pass_context = True,
)
async def biscuit(context):
    await playMP3(beautifulSongsDict['biscuit'], validChannelNames, context)

"""
ButteryBiscuitShort
plays the opening riff from ButteryBiscuitBase
"""
@bot.command(
    name = 'shortbiscuit',
    aliases = ['ShortBiscuit'],
    description = 'All your biscuit...',
    pass_context = True,
)
async def shortbiscuit(context):
    await playMP3(beautifulSongsDict['shortbiscuit'], validChannelNames, context)

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
    'biscuit': '/ButteryBiscuitBot/pythbot/Music/ButteryBiscuitBase.mp3',
    'washington': '/ButteryBiscuitBot/pythbot/Music/Washington.mp3'
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