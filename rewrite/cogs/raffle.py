import sqlite3


class Raffle:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
        self.entries = []
        self.raffle_live = False

    
    @yeebot.group(pass_context=True,
                      description='Start a raffle.')
    async def raffle(self, ctx):
        if ctx.invoked_subcommand is None:
            return await yeebot.say('What do you want to do with the raffle? `!help raffle` for more information.')

    @raffle.command()
    async def start(award_amount):
        pass

    @raffle.command()
    async def end():
        pass

    @raffle.command()
    async def enter():
        pass

    @raffle.command()
    async def entries():
        pass


def setup(yeebot):
    yeebot.add_cog(Raffle(yeebot))
