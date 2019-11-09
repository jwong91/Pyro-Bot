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
import emojiList as emoji
import eventList
import calendarInterface as calendar

#Init 
#TODO: add event via calendar api, add list event bot command 
#TODO: deal with dates and times as their parts (i.e. minutes and hours) in dictionaries
#TODO: add error catching
#TODO: implement verifyTime
#TODO: get multiword user input
#! Event input looks like this, with '()' meaning optional: (year), start month, start day, (end month), (end day) 
#! event input, cont.: start hour, start minute, end hour, end minute  

commands = (
    'cogs.event'
)

botLastMsg = None

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = ('?') #Eventually put this into a config file

bot = c.Bot(command_prefix=(BOT_PREFIX))

#Bot code

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
        # await bot.logout()
 
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        global botLastMsg
        botLastMsg = ctx
        return

    print('------------------------------------')
    print('Author: ' + str(ctx.author))
    print('ID: ' + str(ctx.author.id))
    print(ctx.content)
    print('------------------------------------')

    author = str(ctx.author.id)
    if author == '355464236899631115':
        await ctx.channel.send('go write your college apps <:face:627141817678168064>')
    # if author == '285952812683362306':
    #     await ctx.channel.send('dunkan')
    await bot.process_commands(ctx)
    
async def getLastMessage(ctx):
    await ctx.channel.send(str(ctx.channel.fetch_message('633395936751648774')))
    return lambda ctx : str(ctx.channel.fetch_message(int(ctx.channel.last_message_id)))
     
    # return str(ctx.channel.fetch_message(int(ctx.chanel.last_message_id)))

@bot.command()
async def listEvents(ctx):
    print(eventList.eventList)

@bot.command()
async def test(ctx):
    await ctx.send('msg 1')
    await ctx.send('msg 2')
    await ctx.send('emote this msg')
    print(botLastMsg.content)
    await botLastMsg.add_reaction('👍')

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

    await eCreate.handleEvent(ctx, title, eCreate.parseDate(ctx, date), sTime, eTime, desc)
    try:   #! can remove if bot sends a welcome message
        await botLastMsg.add_reaction(emoji.thumbsUp)
        await botLastMsg.add_reaction(emoji.thumbsDown)
    except:
        print('ERROR: No valid bot msg')

@bot.command(name='listAllEvents')
async def listEvents(ctx):
    await calendar.listAllEvents(ctx)
    await ctx.send('Getting all events...')

@bot.command(name='quit')
async def bot_quit(ctx):
    await ctx.send('Bot is shutting down')
    await bot.logout()


bot.run(token)