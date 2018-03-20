import sqlite3
from discord.ext import commands
from bank import Bank

memebuck = '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]'


def account_exists(ctx):
    return Bank.check_if_exists(ctx.message.author.id)

class Memebucks:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
    
    @commands.group(pass_context=True)
    async def memebucks(self, ctx):
        
        if not Bank.check_if_exists(ctx.message.author.id):
            self.cur.execute("INSERT INTO users (user_id, username, meme_bucks) VALUES (?,?,?);",
                             (sender.id, sender.name, 100))
            self.conn.commit()
            return await self.yeebot.say('Congratulations! You have establish'
                                         'ed an account with the Bank of Meme'
                                         'rica! Your account balance is\n{} *'
                                         '*100** {}'
                                         .format(memebuck, memebuck))
        else:
            self.yeebot.say('What would you like to do with memebucks? !help memebucks for more.')
    
    @commands.check(account_exists)
    @memebucks.command(pass_context=True)
    async def balance(self, ctx):
        balance = Bank.check_balance()
        self.yeebot.say('{}, your balance is {}.'.format(ctx.message.author.name, balance))
    
    @commands.check(account_exists)
    @memebucks.command(pass_context=True)
    async def give(self, ctx, user, amount):
        balance = Bank.check_balance()
        if balance >= amount:
            Bank.transfer(ctx.message.author.id, user.id, amount)
            self.yeebot.say('{} memebucks given to {}.'.format(amount, user.name))


def setup(yeebot):
    yeebot.add_cog(Memebucks(yeebot))
