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

    @commands.command(pass_context=True, hidden=True)
    async def reqstats(self, ctx):
        channel = ctx.message.channel
        
        names = []
        times_memed = []

        self.cur.execute("SELECT username, memes_requested FROM users ORDER BY memes_requested DESC LIMIT 5;")

        rows = self.cur.fetchall()
        for row in rows:
            names.append(row[0])
            times_memed.append(row[1])
        
        
        yeestring = 'Memes Requested:\n```\n'
        for x in range(0, len(names)):
            yeestring += '{}: {}\n'.format(names[x], times_memed[x])
        yeestring += '```'

        return await self.yeebot.say(yeestring)
        



    @commands.command(pass_context=True, hidden=True)
    async def substats(self, ctx):
        channel = ctx.message.channel

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
        width = 0.4
        approved_bar = plt.bar(N, approved, width, color="green", edgecolor = "none")
        rejected_bar = plt.bar(N, rejected, width, color="red", bottom=approved, edgecolor="none")

        bars = [rejected_bar, approved_bar]
        
        counter = 0
        bar_counter = 0

        bar_heights = []
        percentages = []

        for x in range(0, len(approved)):
            percentages.append(int(100 * (approved[x] / (approved[x] + rejected[x]))))

        for container in rejected_bar:
            bar_heights.append(container.get_height())
        for container in approved_bar:
            bar_heights[counter] = bar_heights[counter] + container.get_height()
            counter += 1
        for container in approved_bar:
            plt.text(container.get_x() + container.get_width() + 0.02, bar_heights[bar_counter] / 2, str(int(bar_heights[bar_counter])), ha='left', va='center')
            bar_counter += 1

        for bar in bars:
            for container in bar:
                height = container.get_height()
                y = container.get_y()
                width = container.get_width()
                x = container.get_x()
                plt.text(x + (width / 2), y + (height / 2), str(int(height)), ha='center', va='center')
                

        plt.title('Top 5 Submitters by Volume')
        plt.ylabel('# Memes Submitted')
        plt.xticks(N, names)
        
        plt.figlegend((approved_bar, rejected_bar),
                      ('Approved', 'Rejected'),
                      'upper right')
        plt.savefig('cogs/output/stats.png')
       
        yeestring = '```\n'
        for x in range(0, len(names)):
            yeestring += '{}: {}% approval rate.\n'.format(names[x], percentages[x])
        yeestring += '```'
        
        await self.yeebot.send_file(channel, 'cogs/output/stats.png')
        return await self.yeebot.say(yeestring)

def setup(yeebot):
    yeebot.add_cog(Stats(yeebot))
