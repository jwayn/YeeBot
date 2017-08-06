from discord.ext import commands
import discord
import sqlite


class Raffle:
    raffle_live = False
    entries = []
    initiator_name = ''
    initiator_id = 0
    
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite.connect('db/yee.db')
        self.cur = self.conn.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS raffles (raffle_id INTEGER PRIMARY KEY, initiator_name TEXT,"
                         " initiator_id TEXT, time_started TEXT DEFAULT datetime('now'), winner_name TEXT, "
                         "winner_id TEXT, winnings_amount)")
        
        self.cur.execute('CREATE TABLE IF NOT EXISTS raffle_entries (raffle_id INTEGER REFERENCES raffles(raffle_id),'
                         ' user_id TEXT, user_name TEXT, is_winner INTEGER DEFAULT 0, UNIQUE (raffle_id, user_id))')
        
    @commands.group(pass_context=True,
                      description='Start a raffle.')
    async def raffle(self, ctx):
        if Raffle.raffle_live:
            return await self.yeebot.say(f'There if a live raffle started by {initiator} at {start_time}. There are currently {num_entries} raffle entries.')
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
