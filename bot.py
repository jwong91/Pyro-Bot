import discord as dc 
import os
from dotenv import load_dotenv
import functions as fn

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = dc.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if message.content == '?set event':
        print("Event received!")
        # await message.channel.send("please enter the date")
        await fn.pingMessage(message.content)


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)