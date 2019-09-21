import discord as dc 
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = dc.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# async def on_message():
#     print("Message received!")

client.run(token)