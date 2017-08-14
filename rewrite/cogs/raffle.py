from discord.ext import commands
import discord
import sqlite3
import secrets


def is_admin(ctx):
    roles = ctx.message.author.roles
    for role in secrets.ADMIN_ROLES:
        if role in roles:
            return True
    return False


class Raffle:
    
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS raffles (raffle_id INTEGER PRIMARY KEY, is_live INTEGER," 
                         " initiator_id TEXT, initiator_name TEXT, time_started TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                         " winner_id TEXT, winner_name TEXT, winnings_amount INTEGER)")
        
        self.cur.execute('CREATE TABLE IF NOT EXISTS raffle_entries (raffle_id INTEGER REFERENCES raffles(raffle_id),'
                         ' user_id TEXT, user_name TEXT, is_winner INTEGER DEFAULT 0, UNIQUE (raffle_id, user_id))')
        self.conn.commit()

        # Check if there is already a live raffle in the database
        self.cur.execute('SELECT * FROM raffles WHERE is_live = 1')
        
        fetch = self.cur.fetchone()

        if fetch:
            self.is_live = 1
            self.live_raffle_id = fetch[0]
            self.initiator = fetch[1]
            self.time_started = fetch[3]
        else:
            self.is_live = 0

    @commands.group(pass_context=True)
    async def raffle(self, ctx):
        if ctx.invoked_subcommand is None:
            return await self.yeebot.say('What do you want to do with the raffle? `!help raffle` for more information.')

    @commands.check(is_admin) 
    @raffle.command(name='start', description='Start a raffle with `!raffle start <award_amount>`')
    async def start(self, ctx, award_amount=None):
        if award_amount:
            self.cur.execute('INSERT INTO raffles (is_live, initiator_id, initiator_name, winnings_amount) VALUES'
                             ' (1, ?, ?, ?)', ctx.message.author.id, ctx.message.author.name, award_amount)
            self.is_live = True
        else: 
            self.cur.execute('INSERT INTO raffles (is_live, initiator_id, initiator_name, winnings_amount) VALUES'
                             ' (1, ?, ?, 0)', ctx.message.author.id, ctx.message.author.name)
            self.is_live = True

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
