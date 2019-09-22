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

@client.event
async def on_message(message):
    print(message.content)
    mEvents.messageEventsFunc(message)


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)