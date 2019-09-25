import discord as dc 
import os
from dotenv import load_dotenv
import messageEvents as mEvents

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = dc.Client()


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
    if message.content.startswith('?'):
        await mEvents.handleMessage(message, message.content, user, message.author.id)


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)