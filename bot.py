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
    print(message.content)
    print(message)
    await mEvents.handleMessage(message, message.content)
    # await mEvents.handleMessage(message, message.content)


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)