import discord as dc
import random as rand
import prepFuncts as fn

client = dc.Client()

boomerYesCount = 0
boomerNoCount = 0

atUser = lambda user : '<@' + user + '>'

@client.event
async def handleMessage(message, messageContent, user, authorID, mentionedUser):
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

    global boomerNoCount
    global boomerYesCount

    if messageContent.startswith('?boomer'):
        boomer = rand.randint(0, 1)

        if len(str(mentionedUser)) > 0:
            if boomer == 0:
                await message.channel.send('<@' + str(mentionedUser) + '>' + ' is no boomer')
                boomerNoCount += 1
                print(boomerNoCount)
            elif boomer == 1:
                await message.channel.send('<@' + str(mentionedUser) + '>' + ' is yes boomer')
                boomerYesCount += 1
                print(boomerYesCount)
        
        if messageContent == '?boomer':
            if boomer == 0:
                await message.channel.send(atUser(str(authorID)) + ' is no boomer')
                boomerNoCount += 1
                print(boomerNoCount)
            elif boomer == 1:
                await message.channel.send(atUser(str(authorID)) + ' is yes boomer')
                boomerYesCount += 1
                print(boomerYesCount)

        if messageContent == '?boomercount':
            await message.channel.send('yes: ' + str(boomerYesCount))
            await message.channel.send('no: ' + str(boomerNoCount))

    if messageContent in fn.boomerMisspellings:
        await message.channel.send('learn to type, loser' + ' <:face:627141817678168064>')

    print(messageContent)
    print(user)
    # await message.channel.send('@' + user + ' sent a message!')
    # print('pinged message')
    
        

