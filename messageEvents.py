import discord as dc

client = dc.Client()

@client.event
async def messageEventsFunc(messageIn):
    await message.channel.content('You sent a message!')
    print('pinged message')
    print(messageIn)
    if messageIn == '?set event':
        print('Event received!')
        

