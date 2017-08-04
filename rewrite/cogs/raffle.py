from discord.ext import commands
import discord


class Raffle:
    raffle_live = False
    entries = []
    
    def __init__(self, yeebot):
        self.yeebot = yeebot
    
    @commands.group(pass_context=True,
                      description='Start a raffle.')
    async def raffle(self, ctx):
        if ctx.invoked_subcommand is None:
            return await self.yeebot.say('What do you want to do with the raffle? `!help raffle` for more information.')

    @raffle.command(name='start', description='Start a raffle with `!raffle start <number>`')
    async def start(self, award_amount=None):
        if award_amount is None:
            Raffle.raffle_live = True 
            return await self.yeebot.say('Enter an award amount with `!raffle start <number>`')
        else:
            Raffle.raffle_live = True
            return await self.yeebot.say('Start a raffle')

    @raffle.command(name='end')
    async def end(self):
        return await self.yeebot.say('End a raffle')

    @raffle.command(name='enter')
    async def enter(self):
        return await self.yeebot.say('Enter a raffle')

    @raffle.command(name='entries')
    async def entries(self):
        return await self.yeebot.say('Show all entries of the raffle')


def setup(yeebot):
    yeebot.add_cog(Raffle(yeebot))
