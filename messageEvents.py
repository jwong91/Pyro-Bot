import discord as dc
import random as rand
import prepFuncts as fn
import asyncio
# import emojiList as emoji

boomerNo = 0
boomerYes = 0


async def handle_boomer(ctx, author, mentioned_user, *arg):
    global boomerNo
    global boomerYes

    b_chance = rand.randint(0,1)
    if len(arg) == 0 and not b_chance:
        await ctx.send('you are not pyropal, ' + '<@' + str(author) + '>')
        boomerNo += 1

    elif len(arg) == 0 and b_chance:
        await ctx.send('you are pyropal, ' + '<@' + str(author) + '>')
        boomerYes += 1

    elif len(str(mentioned_user)) > 0 and b_chance == 0:
        await ctx.send('<@' + str(mentioned_user) + '>' + ' is not pyropal')
        boomerNo += 1
        print(arg)
        print(len(arg))

    elif len(str(mentioned_user)) > 0 and b_chance == 1:
        await ctx.send('<@' + str(mentioned_user) + '>' + ' is pyropal')
        boomerYes += 1


async def handle_boomer_count(ctx):
    await ctx.send('yes: ' + str(boomerYes))
    await ctx.send('no: ' + str(boomerNo))



