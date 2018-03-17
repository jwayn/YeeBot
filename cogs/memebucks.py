import sqlite3
from discord.ext import commands

memebuck = '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]'


class Memebucks:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
    
    @commands.group(pass_context=True)
    async def memebucks(self, ctx):

        sender = ctx.message.author
        self.cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?;",
                         (sender.id,))
        row = self.cur.fetchone()
        if row:
            return await self.yeebot.say('{}, your balance is {} memebucks.'
                                         .format(sender.name, row[0]))
        else:
            self.cur.execute("INSERT INTO users (user_id, username, meme_buck"
                             "s) VALUES (?,?,?);",
                             (sender.id, sender.name, 100))
            self.conn.commit()
            return await self.yeebot.say('Congratulations! You have establish'
                                         'ed an account with the Bank of Meme'
                                         'rica! Your account balance is\n{} *'
                                         '*100** {}'
                                         .format(memebuck, memebuck))

    @memebucks.command(pass_context=True)
    async def balance(self, ctx):
        pass

    @memebucks.command(pass_context=True)
    async def give(self, ctx, user, amount):
        pass


def setup(yeebot):
    yeebot.add_cog(Memebucks(yeebot))
