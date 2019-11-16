import discord as dc 
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import prepFuncts as fn
# import eventCreator 
import messageEvents as mEvents
import polls 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?') #Eventually put this into a config/.env file

bot = commands.Bot(command_prefix=(BOT_PREFIX))



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    print('Bad command: ' + ctx.message.content)
    if ctx.message.content in fn.boomerMisspellings:
        await ctx.send('learn to type, boomer' + ' <:face:627141817678168064>')
    else:
        await ctx.send('learn to type, loser' + ' <:face:627141817678168064>')

 
    
@bot.command()
async def boomer(ctx, *arg):
    author = ctx.author.id
    try:
        mentionedUser = ctx.message.mentions[0].id
    except:
        mentionedUser = ''
    await mEvents.handleBoomer(ctx, author, mentionedUser, *arg)
    print(ctx.author.id)

@bot.command()
async def boomercount(ctx, arg='()'):
    if arg != '()':
        return
    await mEvents.handleBoomercount(ctx)


@bot.command(name='poll')
async def createPoll(ctx, *arg):
    details = []
    for arg in arg:
        details = details[arg]
        print(details)
    await polls.createPoll(ctx, details)

bot.run(token)