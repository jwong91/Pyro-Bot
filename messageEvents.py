import discord as dc

client = dc.Client()


def messageEventsFunc(messageIn):
    messageIn.channel.send("test")
    print("pinged message")

