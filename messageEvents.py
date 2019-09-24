import discord as dc

client = dc.Client()

@client.event
async def handleMessage(message, messageContent):
    print(message)
    print(messageContent)
    await message.channel.send('You sent a message!')
    print('pinged message')
    
        

