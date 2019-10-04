import discord as dc 

#Input: ?event date (mm/dd/yy (optional)), starttime (pm/am), endtime (pm/am), description
# Separated by ':'

async def parseEventInput(input): #Parses string into date, time, and description. 
    eventData = input.split(':')
    date = eventData[1]
    sTime = eventData[2]
    eTime = eventData[3]
    description = eventData[4]
    return sTime, eTime, date, description

async def createEvent(date, time, description): 
    return