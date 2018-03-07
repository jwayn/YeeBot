from discord.ext import commands
from memebucks import Memebucks
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


    @color.command(name='teal', description="Change name color to teal.", pass_context=True)
    async def teal(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' teal' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='teal')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is teal. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='green', description="Change name color to green.", pass_context=True)
    async def green(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' green' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='green')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is green. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='blue', description="Change name color to blue.", pass_context=True)
    async def blue(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' blue' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='blue')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is blue. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='purple', description="Change name color to purple.", pass_context=True)
    async def purple(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' purple' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='purple')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is purple. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='red', description="Change name color to red.", pass_context=True)
    async def red(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' red' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='red')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is red. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='yellow', description="Change name color to yellow.", pass_context=True)
    async def yellow(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' yellow' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='yellow')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is yellow. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='orange', description="Change name color to orange.", pass_context=True)
    async def orange(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' orange' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='orange')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is orange. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='grey', description="Change name color to grey.", pass_context=True)
    async def grey(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 100:
            print('enough memebucks')
            if ' grey' in ctx.message.author.roles:
                return await self.yeebot.say('You are already that color, silly.')
            else:
                role = discord.utils.get(ctx.message.server.roles, name='grey')
                await self.yeebot.replace_roles(ctx.message.author, role)
               #Memebucks.withdraw(self, ctx.message.author.id, 100)
                return await self.yeebot.say('Your new color is grey. Your new balance is {}'.format(Memebucks.check_balance(self, ctx.message.author.id)))
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 100 memebucks to change the color of your name. Get out there and submit some memes!')

def setup(yeebot):
    yeebot.add_cog(Colors(yeebot))
