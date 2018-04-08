import sqlite3
import discord
from discord.ext import commands
from bank import Bank

memebuck = '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]'

bank = Bank()

def account_exists(ctx):
    return bank.check_if_exists(ctx.message.author.id)

class Memebucks:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor() 
    
    @commands.group(pass_context=True)
    async def memebucks(self, ctx):
       
        if ctx.invoked_subcommand is None:    
            if bank.check_if_exists(ctx.message.author.id):
                return await self.yeebot.say('What would you like to do with memebucks? !help memebucks for more.') 
            else:
                self.cur.execute("INSERT INTO users (user_id, username, meme_bucks) VALUES (?,?,?);",
                                 (ctx.message.author.id, ctx.message.author.name, 100))
                self.conn.commit()
                return await self.yeebot.say('Congratulations! You have establish'
                                             'ed an account with the Bank of Meme'
                                             'rica! Your account balance is\n{} *'
                                             '*100** {}'
                                             .format(memebuck, memebuck))
    
    @commands.check(account_exists)
    @memebucks.command(pass_context=True, description='Check your memebucks balance.' )
    async def balance(self, ctx):
        balance = bank.check_balance(ctx.message.author.id)
        return await self.yeebot.say('{}, your balance is {}.'.format(ctx.message.author.name, balance))
   
    @commands.check(account_exists)
    @memebucks.command(pass_context=True, description='Give some of your memebucks to someone else. !memebucks give <@user_mention> <amount to give>')
    async def give(self, ctx, user:discord.User, amount:int):
        balance = bank.check_balance(ctx.message.author.id)
        if balance >= amount:
            if bank.check_if_exists(user.id):
                bank.transfer(ctx.message.author.id, user.id, amount)
                return await self.yeebot.say('{} memebucks given to {}.'.format(amount, user.name))
            else:
                return await self.yeebot.say("That user hasn't made an account yet! No memebucks transferred.")
        else:
            return await self.yeebot.say('Sorry, you need more memebucks to do that.')


def setup(yeebot):
    yeebot.add_cog(Memebucks(yeebot))
