from discord.ext import commands
import discord
import sqlite3
import secrets
import random

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
    @raffle.command(name='start', description='Start a raffle with `!raffle start <optional_award_amount>`')
    async def start(self, ctx, award_amount=None):
        if award_amount:
            self.cur.execute('INSERT INTO raffles (is_live, initiator_id, initiator_name, winnings_amount) VALUES'
                             ' (1, ?, ?, ?)', ctx.message.author.id, ctx.message.author.name, award_amount)
            self.is_live = 1
        else: 
            self.cur.execute('INSERT INTO raffles (is_live, initiator_id, initiator_name, winnings_amount) VALUES'
                             ' (1, ?, ?, 0)', ctx.message.author.id, ctx.message.author.name)
            self.is_live = 1

    @commands.check(is_admin)
    @raffle.command(name='end')
    async def end(self, ctx):
        #check if raffle already live
        self.cur.execute("SELECT raffle_id, winnings_amount FROM raffles WHERE is_live = 1;")
        row = self.cur.fetchone()
        raffle_id = row[0]
        winnings_amoung = row[1]
        #if raffle is live 
        if raffle_id:
        #   pick raffle winner
            self.cur.execute("SELECT user_id FROM raffle_entries WHERE raffle_id = ?", (raffle_id,))
            entries = self.cur.fetchall()
            winner_id = random.choice(entries)
        #   if there is an amount to win    
            if winnings_amount:
        #        award winner with award amount
                if Memebucks.check_if_exists(self, winner_id):
                    Memebucks.deposit(self, winnings_amount, winner_id)
                    return await self.yeebot.say('Congratulations, {}! You have won the raffle, and have been awarded {} memebucks!'.format(pass, winnings_amount))
                else:
                    return await self.yeebot.say('No account = no money!') 
        #        
        else:
        #   return message stating to start raffle
            return await self.yeebot.say('There is no live raffle. Please start a raffle.')

    @raffle.command(name='enter')
    async def enter(self, ctx):
       #check if user is already in raffle
       #if user is in raffle
       #    return message that says user is in raffle already
       #else
       #    enter user into raffle

    @commands.check(is_admin)
    @raffle.command(name='entries')
    async def entries(self, ctx):
        #return list of users in raffle

def setup(yeebot):
    yeebot.add_cog(Raffle(yeebot))
