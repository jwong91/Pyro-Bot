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
import memberList

# TODO: Rework event creation GUI
# TODO: Add options to add relevant links to events
# TODO: Add options to add relevant images to events
# TODO: Fix listallevents
# TODO: deal with dates and times as their parts (i.e. minutes and hours) in dictionaries
# TODO: implement verify_time
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
# TODO: Fix bug that creates an event message when invalid values are input

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
BOT_PREFIX = '!'  # Eventually put this into a config file

bot = c.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    print('Bad command: ' + ctx.message.content)
    if ctx.message.content in fn.boomerMisspellings:
        await ctx.send('Pyro command error')
    else:
        traceback.print_exc()
        await ctx.send('Command error ' + '(' + str(error) + ')')
        # await bot.logout()


@bot.event
async def on_error(error, *args, **kwargs):
    traceback.print_exc()


@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        global botLastMsg
        botLastMsg = ctx
        eCreate.update_bot_last_msg(ctx)
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
    # if author == '355464236899631115':
    #     await ctx.channel.send('_ _\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n_ _')

    # if author == '285952812683362306':
    #     await ctx.channel.send('dunkan')
    await bot.process_commands(ctx)


@bot.event
async def on_raw_reaction_add(ctx):
    if ctx.user_id in fn.bannedAttendeesList:
        return

    print('reaction detected!')
    print('reaction ' + ' was added by ' + str(ctx.user_id))

    for member in bot.get_all_members():
        memberList.memberList[member.id] = member.display_name
    # print(memberList.memberList)

    guest_id = ctx.user_id
    event_id = None

    guest_name = memberList.memberList[guest_id]

    try:
        try:
            event_id = str(ctx.message_id)
            event_file = 'event-database/' + event_id + '.json'
        except:
            print('invalid event ID likely caused by non-event message being emoted')

        with open(event_file, 'r') as idList:
            event_details = json.load(idList)
            if event_id == str(event_details['eventID']):
                event_name = event_details['title']
                if str(ctx.emoji) == emoji.thumbsUp:
                    await calendar.add_rsvp(event_name, event_id, guest_name)
                elif str(ctx.emoji) == emoji.thumbsDown:
                    await calendar.add_not_going(event_name, event_id, guest_name)
                elif str(ctx.emoji) == emoji.maybe:
                    await calendar.add_maybe_going(event_name, event_id, guest_name)
    except:
        traceback.print_exc()
    finally:
        idList.close()


@bot.event
async def on_raw_reaction_remove(ctx):
    if ctx.user_id in fn.bannedAttendeesList:
        return

    print('reaction was removed by ' + str(ctx.user_id))

    for member in bot.get_all_members():
        memberList.memberList[member.id] = member.display_name
    # print(memberList.memberList)

    guest_id = ctx.user_id
    event_id = str(ctx.message_id)
    guest_name = memberList.memberList[guest_id]
    event_file = 'event-database/' + event_id + '.json'

    with open(event_file, 'r') as idList:
        event_details = json.load(idList)

        if event_id == str(event_details['eventID']):
            event_name = event_details['title']

            if str(ctx.emoji) == emoji.thumbsUp:
                await calendar.remove_rsvp(event_name, event_id, guest_name)
            elif str(ctx.emoji) == emoji.thumbsDown:
                await calendar.remove_not_going(event_name, event_id, guest_name)
            elif str(ctx.emoji) == emoji.maybe:
                await calendar.remove_maybe_going(event_name, event_id, guest_name)


async def get_last_message(ctx):
    await ctx.channel.send(str(ctx.channel.fetch_message('633395936751648774')))
    return lambda ctx: str(ctx.channel.fetch_message(int(ctx.channel.last_message_id)))

    # return str(ctx.channel.fetch_message(int(ctx.chanel.last_message_id)))


@bot.command(name='help')
async def manual_page(ctx, desired_page='all'):
    case = {
        'all': '```All commands: \
            \n help - Lists this help message. For more information on particular commands, type ?help [COMMAND] \
            \n pyro - Checks to see if the user or specified user is a Pyropal \
            \n pyrocount - Counts the number of times pyro has been used \
            \n event - Creates an event \
            \n listallevents - Lists all the events on the calendar \
            \n going - Lists the people who have marked their attendance on an event```',

        'help': '``` Name: help \
                \n Usage: ?help [COMMAND] \
                \n Example: ?help pyro - Shows the help page for the pyro command \
                \n Description: By default, it lists all commands that are available to users. \
                             \n If a command is specified, it will show more information relating to the specified command.```',

        'pyro': '``` Name: pyro \
         \n Usage: ?pyro [USER] \
         \n Example: ?pyro @Rob - Checks to see if Rob is a pyropal \
         \n Description: By default, it checks to see if the user is a pyropal. \
                      \n If a user is specified, the bot will check to see if they are a pyropal.```',

        'pyrocount': '``` Name: pyrocount \
         \n Usage: ?pyrocount \
         \n Description: Counts the number of times the bot has determined a user to be a pyropal/not a pyropal. ```',

        'event': '``` Name: event \
          \n Usage: ?event [TITLE] [DATE] [START_TIME] [END_TIME] [DESCRIPTION]\
          \n Example: ?event Pyrotech 1/4/2020 6:00 18:00 Pyrotech meeting \
          \n Description: Creates an event with a specified title, date, start time, end time, and description. \
          \n Event details are stored in Google Calendar and attendee details are stored in json files on the host computer. \
          \n Times must be given in 24 hour time. \
          \n If the year is not specified, it defaults to the current calendar year. If the year is specified, it must be a full year (i.e. 1/4/20 does not work but \
          \n 1/4/2020 works.) \
          \n Events currently cannot have their title or date changed after creation. However, times can be changed by editing them in Google Calendar. \
          \n Multi-word arguments such as titles and descriptions must be enclosed in quotation marks, otherwise the bot recognizes them as different arguments.```',

        'listallevents': '``` Name: listallevents \
         \n Usage: ?listallevents \
         \n Description: Lists all events on the calendar, including past ones.```',

        'going': '``` Name: going \
         \n Usage: ?going [EVENT] [DATE] [TYPE_OF_ATTENDEE] \
         \n Example: ?going Pyrotech 1/4/2020 notgoing - Lists everyone who said they were not attending \
         \n Description: Outputs a list of people who have marked their attendance on an event. \
         \n By default, it shows the list of attendees. \
         \n The date is important because it provides a way to differentiate between two events of the same name.```'
    }
    page = case[desired_page.lower()]
    await ctx.send(page)


@bot.command()
async def get_member(ctx):
    print(bot.get_user(362779255634919424))
    print(type(bot.get_user(362779255634919424)))


@bot.command(name='pyro')
async def boomer(ctx, *arg):
    author = ctx.author.id
    try:
        mentioned_user = ctx.message.mentions[0].id
    except:
        mentioned_user = ''
    await mEvents.handle_boomer(ctx, author, mentioned_user, *arg)
    print(ctx.author.id)


@bot.command(name='pyrocount')
async def boomer_count(ctx, arg='()'):
    if arg != '()':
        return
    await mEvents.handle_boomer_count(ctx)


@bot.command()
async def event(ctx, title='()', date='()', s_time='()', e_time='()', desc='()', length_catcher='()'):
    if title == '()':
        await ctx.send('Missing a title')
        return
    if date == '()':
        await ctx.send('Missing a date')
        return
    if s_time == '()':
        await ctx.send('Missing a start time')
        return
    if e_time == '()':
        await ctx.send('Missing an end time')
        return
    if desc == '()':
        await ctx.send('Missing a description')
        return
    if length_catcher != '()':
        await ctx.send('Too many details')
        return

    try:
        await eCreate.handle_event(ctx, title, eCreate.parse_date(ctx, date), s_time, e_time, desc, date)
    except:
        traceback.print_exc()

    try:  # ! can remove if bot sends a welcome message
        sleep(2)  # Sometimes it doesn't emote the last message
        await botLastMsg.add_reaction(emoji.thumbsUp)
        await botLastMsg.add_reaction(emoji.thumbsDown)
        await botLastMsg.add_reaction(emoji.maybe)
    except:
        print('ERROR: No valid bot msg')


@bot.command(name='listAllEvents')
async def list_events(ctx):
    await ctx.send('Getting all events...')
    await calendar.list_all_events(ctx)


@bot.command(name='going')
async def who_is_attending(ctx, title, date, desired_type='going'):
    await calendar.get_attendees(ctx, title, date, desired_type)


@bot.command()
async def rsvp(ctx, desired_event=None):  # Deprecated
    if not desired_event:
        await ctx.send('Please enter an event that you wish to RSVP for.')
        return

    await calendar.rsvp(ctx, desired_event)


@bot.command(name='quit')
async def bot_quit(ctx):
    await ctx.send('Bot is shutting down')
    await bot.logout()


bot.run(token)
