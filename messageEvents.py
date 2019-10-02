import discord as dc
import random as rand
import prepFuncts as fn

async def handleBoomer(ctx, *arg):
    if len(arg) == 0:
        await ctx.send('you are boomer')
    elif len(arg) > 0:
        await ctx.send('they are boomer')
        print(arg)
        print(len(arg))

    
        

