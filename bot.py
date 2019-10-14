import discord as dc 
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands as c
from discord.ext.commands import CommandNotFound
import prepFuncts as fn
import eventCreator as eCreate 
import messageEvents as mEvents
import traceback

# from cogs.utils import checks, context, db

commands = (
    'cogs.event'
)


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?') #Eventually put this into a config/.env file

bot = c.Bot(command_prefix=(BOT_PREFIX))



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
        traceback.print_exc()
        await bot.logout()
 
async def getLastMessage(ctx):
    await ctx.channel.send(str(ctx.channel.fetch_message(int(ctx.channel.last_message_id))))
    return str(ctx.channel.fetch_message(int(ctx.chanel.last_message_id)))

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    print('------------------------------------')
    print('Author: ' + str(ctx.author))
    print(str(ctx.author.id))
    print(ctx.content)
    # await ctx.channel.fetch_message(int(ctx.channel.last_message_id)).add_reaction('👍')
    # await getLastMessage(ctx)
    author = str(ctx.author.id) 
    if author == '355464236899631115':
        await ctx.channel.send('go write your college apps <:face:627141817678168064>')
    # if author == '285952812683362306':
    #     await ctx.channel.send('dunkan')
    await bot.process_commands(ctx)
    
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

@bot.command()
async def event(ctx, title='()', date='()', sTime='()', eTime='()', desc='()', lengthCatcher='()'):
    if title == '()':
        await ctx.send('Missing a title')
        return
    if date =='()':
        await ctx.send('Missing a date')
        return
    if sTime == '()':
        await ctx.send('Missing a start time')
        return
    if eTime == '()':
        await ctx.send('Missing an end time')
        return
    if desc == '()':
        await ctx.send('Missing a description')
        return
    if lengthCatcher != '()':
        await ctx.send('Too many details')
        return

    # await ctx.send('Event details: ' \
    #     + 'Name: ' + title + '  ' \
    #     + 'Date: ' + date + '  ' \
    #     + 'Start time: ' + sTime + '  ' \
    #     + 'End time: ' + eTime + '  ' \
    #     + 'Desciption: ' + desc)
    await mEvents.handleEvent(ctx, title, eCreate.parseDate(ctx, date), sTime, eTime, desc)


@bot.command()
async def bot_quit(ctx):
    await ctx.send('Bot is shutting down')
    await bot.logout()

bot.run(token)