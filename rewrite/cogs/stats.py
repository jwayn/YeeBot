import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import discord
from discord.ext import commands

class Stats:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()

    @commands.command()
    async def whatever(self):
        return await self.yeebot.say('whatever')

    @commands.command(pass_context=True)
    async def substats(self, context):
        channel = context.message.channel

        names = []
        submissions = []
        rejected = []
        approved = []

        self.cur.execute("select submitter_name, count (submitter_name) from links group "
                    "by submitter_name order by count (submitter_name) desc limit 5;")

        rows = self.cur.fetchall()
        for row in rows:
            names.append(row[0])
            submissions.append(row[1])

        for name in names:
            self.cur.execute("select count (*) from links where status = 'approved' and "
                        "submitter_name = ?;", (name,))
            num_appr = self.cur.fetchone()
            approved.append(int(num_appr[0]))
            self.cur.execute("select count (*) from links where status = 'rejected' and "
                        "submitter_name = ?;", (name,))
            num_rej = self.cur.fetchone()
            rejected.append(int(num_rej[0]))

        N = np.arange(len(names))
        width = 0.5
        approved_bar = plt.bar(N, approved, width, color="green", edgecolor = "none")
        rejected_bar = plt.bar(N, rejected, width, color="red", bottom=approved, edgecolor="none")
        plt.title('Memes approved & rejected')
        plt.ylabel('Memes Submitted')
        plt.xticks(N, names)
        plt.figlegend((approved_bar, rejected_bar),
                      ('Approved', 'Rejected'),
                      'upper right')

        plt.savefig('cogs/output/stats.png')

        return await self.yeebot.send_file(channel, 'cogs/output/stats.png')

def setup(yeebot):
    yeebot.add_cog(Stats(yeebot))
