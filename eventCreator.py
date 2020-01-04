import discord as dc
import eventList 
from datetime import datetime
import calendarInterface as calendar
import traceback

# calendarInterface.createCalEvent('test', 'date', 'time', 'time1', 'descHere')

#Input: ?event date (mm/dd/yy (optional)), starttime (pm/am), endtime (pm/am), description
# Separated by ':'


def verifyTime(time):
    try:
        split = time.split('-')
        sTime = int(split[0])
        eTime = int(split[1])
    except:
        print('ERROR: Bad time')

    print(eTime)
    print(sTime)

    if (type(sTime) != int or sTime > 12 or
        type(eTime) != int or eTime > 12):
        print('Bad time')
        return False
    else:
        print('Valid time')
        return True

def verifyDate(date):
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


def parseDate(ctx, date):
    split = date.split('/')
    if len(split) < 3:
            split.append(str(datetime.now().year))
            print(split)

    if not verifyDate(split):
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

    
def createDateTime(date, sTime, eTime):
    # if verifyTime(sTime, eTime):
        # Create a datetime that looks like YYYY-MM-DDTHH:MM:SS
    startDatetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                    + sTime + ':' + '00']
    endDatetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                    + eTime + ':' + '00']

    # print(startDatetime)
    # print(endDatetime)
    return startDatetime, endDatetime

def makeReadableDateTime(dateTime):
    split = dateTime.split('T')
    date = split[0].split('-')
    date[0], date[1] = date[1], date[0]
    date[1], date[2] = date[2], date[1]
    date = ('/').join(date)
    
    time = {'start' : split[1].split('-')[0], 'end' : split[1].split('-')[1]}
    time['start'] = time['start'][:-3]
    
    return date, time

async def handleEvent(ctx, eventId, title, date, sTime, eTime, desc): 
    if not date:
        return

    print('Create Event: ')
    print('Year: ' + date.get('Year'))
    print('Start Time: ' + sTime)
    print('End Time: ' + eTime)
    print('Description: ' + desc)
    print('Creating event: Year: ' + date.get('Year'))

    await ctx.send('Event details:')
    await ctx.send('Title: ' + title)
    await ctx.send('Month: ' + date.get('Month'))
    await ctx.send('Day: ' + date.get('Day'))
    await ctx.send('Year: ' + date.get('Year'))
    await ctx.send('Start Time: ' + sTime)
    await ctx.send('End Time: ' + eTime)
    await ctx.send('Description: ' + desc)


    #add event via google calendar API
    calendar.createCalEvent(title, createDateTime(date, sTime, eTime), desc, eventId)
    try:
        with open('eventIds.txt', mode='a+') as idList:
            idList.write(str(eventId) + '\n')
            print(idList.read())
    except:
        traceback.print_exc()
    finally:
        idList.close()
