from discord.ext import commands
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('bot is ready!')
    channel = bot.get_channel(627968216588746795)
    await channel.send('ready!')


@bot.command()
async def ping(ctx):  # Command is invoked with '?ping', ctx is context arg (i.e. message)
    await ctx.send('pong!')

bot.run(token)
