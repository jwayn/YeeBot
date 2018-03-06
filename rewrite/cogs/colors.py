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


class Colors:
    
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
        
    @commands.group(pass_context=True)
    async def color(self, ctx):
        if ctx.invoked_subcommand is None:
            return await self.yeebot.say('What color do you want to change to? !help colors for more information.')

    @raffle.command(name='teal')
    async def teal(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this

    
    @raffle.command(name='green')
    async def green(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this
    

    @raffle.command(name='blue')
    async def blue(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this


    @raffle.command(name='purple')
    async def purple(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this


    @raffle.command(name='red')
    async def red(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this

    @raffle.command(name='red')
    async def red(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this

    
    @raffle.command(name='yellow')
    async def yellow(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this
    

    @raffle.command(name='orange')
    async def orange(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this


    @raffle.command(name='grey')
    async def grey(self, ctx):
        #change user color to green
        #subtract 100 memebcuks from account
        #return message stating this

def setup(yeebot):
    yeebot.add_cog(Colors(yeebot))
