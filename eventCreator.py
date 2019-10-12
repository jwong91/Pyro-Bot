import discord as dc 


boomerNo = 1
boomerYes = 2
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

    

async def parseEventInput(ctx, input): #Parses string into date, time, and description. 
    print('parsing')
    eventData = input.split(':')
    date = eventData[1]
    sTime = eventData[2]
    eTime = eventData[3]
    description = eventData[4]
    await ctx.send(sTime + eTime + date + description)
    return sTime, eTime, date, description


    