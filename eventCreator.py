import discord as dc
from discord import Client
import eventList
from datetime import datetime
import calendarInterface as calendar
import traceback

# calendarInterface.createCalEvent('test', 'date', 'time', 'time1', 'descHere')

# Input: ?event date (mm/dd/yy (optional)), starttime (pm/am), endtime (pm/am), description
# Separated by ':'

botLastMsg = None


def verify_time(time):
    try:
        split = time.split('-')
        s_time = int(split[0])
        e_time = int(split[1])
    except:
        print('ERROR: Bad time')

    if (type(s_time) != int or s_time > 12 or
       type(e_time) != int or e_time > 12):
        print('Bad time')
        return False
    else:
        print('Valid time')
        return True


def verify_date(date):
    if len(date) > 3:
        print('Invalid date')
        return False

    try:
        for val in date:
            val = int(val)
            return True
    except:
        print('Date contains non-integer values')
        return False


def parse_date(ctx, date):
    split = date.split('/')
    if len(split) < 3:
        split.append(str(datetime.now().year))
        print(split)

    if not verify_date(split):
        return

    try:
        year = split[2]
        month = split[0]
        day = split[1]
        date = {'Year': year, 'Month': month, 'Day': day}
        return date
    except:
        print('invalid date')
        return False


def create_date_time(date, s_time, e_time):
    # if verify_time(s_time, e_time):
    # Create a datetime that looks like YYYY-MM-DDTHH:MM:SS
    start_datetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                      + s_time + ':' + '00']
    end_datetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                    + e_time + ':' + '00']

    # print(start_datetime)
    # print(end_datetime)
    return start_datetime, end_datetime


def make_readable_date_time(date_time):
    split = date_time.split('T')
    date = split[0].split('-')
    date[0], date[1] = date[1], date[0]
    date[1], date[2] = date[2], date[1]
    date = '/'.join(date)

    time = {'start': split[1].split('-')[0], 'end': split[1].split('-')[1]}
    time['start'] = time['start'][:-3]

    return date, time


def update_bot_last_msg(msg):
    global botLastMsg
    botLastMsg = msg


async def handle_event(ctx, title, date, s_time, e_time, desc, raw_date):
    if not date:
        return

    print('Create Event: ')
    print('Year: ' + date.get('Year'))
    print('Start Time: ' + s_time)
    print('End Time: ' + e_time)
    print('Description: ' + desc)
    print('Creating event: Year: ' + date.get('Year'))

    event_message = dc.Embed(title=title, description=desc, color=0xFF0000)  # 0xFF0000 is red
    event_message.set_author(name='Event')
    event_message.add_field(name='*Date*', value='/'.join([date.get('Month'), date.get('Day'), date.get('Year')]))
    event_message.add_field(name='*Time*', value='-'.join([s_time, e_time]), inline=False)

    await ctx.send(embed=event_message)

    try:
        event_id = str(botLastMsg.id)
        # Add event via google calendar API
        calendar.create_cal_event(title, create_date_time(date, s_time, e_time), desc, event_id, raw_date)
    except:
        event_id = None
        traceback.print_exc()
