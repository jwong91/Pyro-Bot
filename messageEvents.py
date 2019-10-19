import discord as dc
import random as rand
import prepFuncts as fn
import asyncio 
import bot
# import emojiList as emoji

boomerNo = 0
boomerYes = 0





async def handleBoomer(ctx, author, mentionedUser, *arg):
    global boomerNo
    global boomerYes

    bChance = rand.randint(0,1)
    if len(arg) == 0 and bChance == False:
        await ctx.send('you are not boomer, ' + '<@' + str(author) + '>')
        boomerNo += 1

    elif len(arg) == 0 and bChance == True:
        await ctx.send('you are boomer, ' + '<@' + str(author) + '>')
        boomerYes += 1

    elif len(str(mentionedUser)) > 0 and bChance == 0:
        await ctx.send('<@' + str(mentionedUser) + '>' + ' is not boomer')
        boomerNo += 1
        print(arg)
        print(len(arg))

    elif len(str(mentionedUser)) > 0 and bChance == 1:
        await ctx.send('<@' + str(mentionedUser) + '>' + ' is boomer')
        boomerYes += 1

async def handleBoomercount(ctx):
    await ctx.send('yes: ' + str(boomerYes))
    await ctx.send('no: ' + str(boomerNo))


def parseDate(ctx, date):
    print('parsedate')
    split = date.split('/')
    year = split[2]
    month = split[1]
    day = split[0]
    date = {'Year': year, 'Month': month, 'Day': day}
    return str(date)

