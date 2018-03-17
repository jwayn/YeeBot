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
        self.role_colors = ['teal', 'green', 'blue', 'pink', 'purple', 'red',
                       'yellow', 'orange'] 
    
    async def remove_colors(self, ctx):    
        roles = [role for role in ctx.message.author.roles if role.name in
                 self.role_colors]
        if roles:
            await self.yeebot.say('All colors removed, free of charge!')
            return await self.yeebot.remove_roles(ctx.message.author, *roles)

    async def add_color(self, ctx, color):
        roles = [role for role in ctx.message.author.roles if role.name in
                self.role_colors]
        if roles:
            await self.yeebot.say('You already have a color! I went ahead and removed it so you can add another one.')
            return await self.yeebot.remove_roles(ctx.message.author, *roles)
        else:
            color_role = discord.utils.get(ctx.message.server.roles, name=color) 
            Memebucks.withdraw(self, ctx.message.author.id, 50)
            await self.yeebot.add_roles(ctx.message.author, color_role) 
            return await self.yeebot.say('Your new color is {}. Your new balance is {}'.format(color, Memebucks.check_balance(self, ctx.message.author.id)))


    @commands.group(pass_context=True)
    async def color(self, ctx):
        if ctx.invoked_subcommand is None:
            return await self.yeebot.say('What color do you want to change to? !help color for more information.')

    @color.command(name='remove', description="Remove your color.", pass_context=True)
    async def remove(self, ctx):
        return await self.remove_colors(ctx)

    @color.command(name='teal', description="Change name color to teal.", pass_context=True)
    async def teal(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            return await self.add_color(ctx, 'teal')
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='green', description="Change name color to green.", pass_context=True)
    async def green(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'green')
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='blue', description="Change name color to blue.", pass_context=True)
    async def blue(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'blue')
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='purple', description="Change name color to purple.", pass_context=True)
    async def purple(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            await self.add_color(ctx, 'purple')
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='red', description="Change name color to red.", pass_context=True)
    async def red(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'red')
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='yellow', description="Change name color to yellow.", pass_context=True)
    async def yellow(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'yellow') 
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')


    @color.command(name='orange', description="Change name color to orange.", pass_context=True)
    async def orange(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'orange') 
        else:
            print('Not enough memebucks')
            return await self.yeebot.say('You need at least 50 memebucks to change the color of your name. Get out there and submit some memes!')

    @color.command(name='pink', description="Change name color to pink.", pass_context=True)
    async def pink(self, ctx):
        #select memebucks from user
        if Memebucks.check_balance(self, ctx.message.author.id) >= 50:
            print('enough memebucks')
            await self.add_color(ctx, 'pink') 
        else:
            print('Not enough memebucks')
    
def setup(yeebot):
    yeebot.add_cog(Colors(yeebot))
