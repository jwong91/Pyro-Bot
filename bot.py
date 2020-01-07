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
from time import sleep
import event as ev
import json

# TODO: deal with dates and times as their parts (i.e. minutes and hours) in dictionaries
# TODO: implement verifyTime
# TODO: get multi word user input

# TODO: Add formatting to outputs of listAllEvents, etc.
# TODO: Add rsvp (2 commands- add rsvp and remove rsvp)*^
# TODO: Add delete event command
# TODO: Add get x upcoming events command
# TODO: Write help command
# TODO: Add search for event command
# TODO: General cleanup^
# TODO: Add edit event command*
# TODO: Make listEvent list to have the next event at the bottom^
# TODO: Allow for 2 digit years (i.e. 19 = 2019)*^
# TODO: Allow for 12h time input*^
# TODO: Fix bug that doesn't output event times correctly

# RSVP implementation:
# Emoji based
# On event creation, new event ID is the summary - IS NOW MESSAGE ID
# To handle duplicate events, the new event ID is event name + date OR the id of the message
# On emote, check if the message is an event creation message
# If yes, get the summary and search the google api for that

# ! Event input looks like this, with '()' meaning optional: (year), start month, start day, (end month), (end day)
# ! start hour, start minute, end hour, end minute

commands = (
    'cogs.event'
)

botLastMsg = None
userLastMsg = None

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = '?' # Eventually put this into a config file

bot = c.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    print('Bad command: ' + ctx.message.content)
    if ctx.message.content in fn.boomerMisspellings:
        await ctx.send('learn to type, boomer' + ' <:face:627141817678168064>')
    else:
        traceback.print_exc()
        await ctx.send('learn to type, loser' + ' <:face:627141817678168064>')
        # await bot.logout()

@bot.event
async def on_error(error, *args, **kwargs):
    traceback.print_exc()

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        global botLastMsg
        botLastMsg = ctx
        eCreate.updateBotLastMsg(ctx)
        return
    else:
        global userLastMsg
        userLastMsg = ctx

    print('------------------------------------')
    print('Author: ' + str(ctx.author))
    print('ID: ' + str(ctx.author.id))
    print(ctx.content)
    print('------------------------------------')

    author = str(ctx.author.id)
    if author == '355464236899631115':
        await ctx.channel.send('_ _\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n_ _')

    # if author == '285952812683362306':
    #     await ctx.channel.send('dunkan')
    await bot.process_commands(ctx)

@bot.event
async def on_raw_reaction_add(ctx):
    print('reaction detected!')
    print('reaction ' + ' was added by ' + str(ctx.user_id))

    guest = ctx.user_id
    eventId = None
    try:
        eventId = str(ctx.message_id)
        eventFile = 'event-database/' + eventId + '.json'
        with open(eventFile, 'r') as idList:
            eventDetails = json.load(idList)
            if eventId in eventDetails:
                eventName = idList['title']
                calendar.addRsvp(eventName, eventId, guest)
    # except:
        # traceback.print_exc()
    finally:
        idList.close()


async def getLastMessage(ctx):
    await ctx.channel.send(str(ctx.channel.fetch_message('633395936751648774')))
    return lambda ctx : str(ctx.channel.fetch_message(int(ctx.channel.last_message_id)))
     
    # return str(ctx.channel.fetch_message(int(ctx.chanel.last_message_id)))

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
    if date == '()':
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

    try:
        await eCreate.handleEvent(ctx, title, eCreate.parseDate(ctx, date), sTime, eTime, desc)
    except:
        traceback.print_exc()

    try:   # ! can remove if bot sends a welcome message
        sleep(0.5) # Sometimes it doesn't emote the last message
        await botLastMsg.add_reaction(emoji.thumbsUp)
        await botLastMsg.add_reaction(emoji.thumbsDown)
    except:
        print('ERROR: No valid bot msg')


@bot.command(name='listAllEvents')
async def listEvents(ctx):
    await ctx.send('Getting all events...')
    await calendar.listAllEvents(ctx)

@bot.command()
async def rsvp(ctx, desiredEvent=None):
    if not desiredEvent:
        await ctx.send('Please enter an event that you wish to RSVP for.')
        return
    
    await calendar.rsvp(ctx, desiredEvent)

@bot.command(name='quit')
async def bot_quit(ctx):
    await ctx.send('Bot is shutting down')
    await bot.logout()


bot.run(token)
