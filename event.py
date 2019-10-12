from discord.ext import commands

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def testcmd(self, ctx):
        ctx.send('testedcmd')