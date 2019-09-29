import discord as dc 

async def parseEventInput(input): #Parses string into date, time, and description. 
    eventData = input.split(' ')
    time = eventData[1]
    date = eventData[2]
    description = eventData[3]
    return time, date, description

async def createEvent(date, time, description): 
    return