import discord as dc
import eventList 
# import calendarInterface 

# calendarInterface.createCalEvent('test', 'date', 'time', 'time1', 'descHere')

#Input: ?event date (mm/dd/yy (optional)), starttime (pm/am), endtime (pm/am), description
# Separated by ':'

def parseDate(ctx, date):
    split = date.split('/')
    try:
        year = split[2]
        month = split[1]
        day = split[0]
        date = {'Year': year, 'Month': month, 'Day': day}
        return date
    except:
        print('invalid date')
        date = {}

    
def verifyTime(sTime, eTime):
    if (type(sTime) != int or sTime > 12 or
        type(eTime) != int or eTime > 12):
        return False
    else:
        return True

def createDateTime(date, sTime, eTime):
    # if verifyTime(sTime, eTime):
        # Create a datetime that looks like YYYY-MM-DDTHH:MM:SS
    startDatetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                    + sTime + ':' + '00']
    endDatetime = [date['Year'] + '-' + date['Month'] + '-' + date['Day'] + 'T'
                    + eTime + ':' + '00']

    print(startDatetime)
    print(endDatetime)


async def handleEvent(ctx, title, date, sTime, eTime, desc): 
    if date == None:
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
    

    print('Event created!')

    

async def parseEventInput(ctx, input): #Parses string into date, time, and description. 
    print('parsing')
    eventData = input.split(':')
    date = eventData[1]
    sTime = eventData[2]
    eTime = eventData[3]
    description = eventData[4]
    await ctx.send(sTime + eTime + date + description)
    return sTime, eTime, date, description

createDateTime({'Year': '2323', 'Month': '03', 'Day': '11'}, '2', '5')

    