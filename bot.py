import discord as dc 
import os
from dotenv import load_dotenv
import messageEvents as mEvents
from discord.ext.commands import Bot

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?')

client = Bot(command_prefix=(BOT_PREFIX))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

dateEntered = False

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user = str(message.author).split('#')[0]
    print(type(user))
    try:
        messageMentions = message.mentions[0].id
    except:
        messageMentions = ''
    
    await mEvents.handleMessage(message, message.content, user, message.author.id, messageMentions)


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)