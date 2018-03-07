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


    @raffle.command(name='teal' description="Change name color to teal.")
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


    @raffle.command(name='green' description="Change name color to green.")
    async def green(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'green' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'green')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is green. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='blue' description="Change name color to blue")
    async def blue(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'blue' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'blue')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is blue. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='purple' description="Change name color to purple.")
    async def purple(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'purple' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'purple')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is purple. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='red' description="Change name color to red.")
    async def red(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'red' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'red')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is red. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='yellow' description="Change name color to purple.")
    async def yellow(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'yellow' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'yellow')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is yellow. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='orange' description="Change name color to orange.")
    async def orange(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'orange' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'orange')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is orange. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @raffle.command(name='grey' description="Change name color to grey.")
    async def grey(self, ctx):
        #select memebucks from user
        if memebucks.check_balance(ctx.message.author.id) >= 100:
            if 'grey' in ctx.message.author.roles:
                self.yeebot.say('You are already that color, silly.')
            else:
                self.yeebot.replace_role(ctx.message.author, 'grey')
                memebucks.withdraw(ctx.message.author.id, 100)
                self.yeebot.say('Your new color is grey. Your new balance is {}'.format(memebucks.check_balance(ctx.message.author.id)))
        else:
            self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')

def setup(yeebot):
    yeebot.add_cog(Colors(yeebot))
