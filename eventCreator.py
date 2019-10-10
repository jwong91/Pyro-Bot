import discord as dc 
import datetime as dt

boomerNo = 1
boomerYes = 2
#Input: ?event date (mm/dd/yy (optional)), starttime (pm/am), endtime (pm/am), description
# Separated by ':'

async def splitMessage(ctx, date):
    split = date.split('/')
    year = split[2]
    month = split[1]
    day = split[0]
    # date = dt.date(year, month, day)
    await ctx.send(str(split))
    await ctx.send(year)
    await ctx.send('messageSplit')
    # return str(date)
    

async def parseEventInput(ctx, input): #Parses string into date, time, and description. 
    print('parsing')
    eventData = input.split(':')
    date = eventData[1]
    sTime = eventData[2]
    eTime = eventData[3]
    description = eventData[4]
    await ctx.send(sTime + eTime + date + description)
    return sTime, eTime, date, description

async def createEvent(date, time, description): 
    return