import discord as dc 
import os
from dotenv import load_dotenv
# import messageEvents as mEvents

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
    if dateEntered:
        await message.channel.send('please enter a time')
    if message.content.startswith('?'):
        print('legit message')
        if message.content == '?set event':
            print('event')
            await message.channel.send('please enter a date')
            dateEntered = True


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     eventDate = message.content
#     print(eventDate)

client.run(token)