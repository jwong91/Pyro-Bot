import discord as dc 
import os
from dotenv import load_dotenv
# import messageEvents as mEvents
from discord.ext.commands import Bot
from discord.ext import commands
# import eventCreator 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?')

bot = commands.Bot(command_prefix=(BOT_PREFIX))
client = dc.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    

dateEntered = False

@bot.command()
async def boomer(ctx, arg):
    print(arg)
    print(ctx)
    await ctx.send(arg)

client.run(token)