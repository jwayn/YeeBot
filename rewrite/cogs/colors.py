from discord.ext import commands
from memebucks import memebucks
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
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'teal' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'teal')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is teal. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')

    
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
