import discord as dc 
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
# import eventCreator 
import messageEvents as mEvents

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?') #Eventually put this into a config/.env file

bot = commands.Bot(command_prefix=(BOT_PREFIX))



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    

@bot.command()
async def boomer(ctx, *arg):
    await mEvents.handleBoomer(ctx, *arg)

bot.run(token)