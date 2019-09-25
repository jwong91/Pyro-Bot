import discord as dc
import random as rand

client = dc.Client()

@client.event
async def handleMessage(message, messageContent, user, authorID):
    # if user == '10mbRAM':
    #     await message.channel.send(user + ' hello')
    # elif user == 'Whole Wheat Orange':
    #     await message.channel.send(user + ' is boomer')
    # else:
    #     await message.channel.send('bruh moment')

    # if messageContent == '?boomer':
    #     if user == '10mbRAM':
    #         await message.channel.send('jason is not boomer')
    #     else:
    #         await message.channel.send('yes boomer')

    if messageContent == '?boomer':
        boomer = rand.randint(0,1)
        if boomer == 0:
            await message.channel.send('<@' + str(authorID) + '>' + ' is no boomer')
        elif boomer == 1:
            await message.channel.send('<@' + str(authorID) + '>' + ' is yes boomer')


    print(messageContent)
    print(user)
    # await message.channel.send('@' + user + ' sent a message!')
    # print('pinged message')
    
        

