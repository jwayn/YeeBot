import sqlite3, re, random, praw, secrets
from discord.ext import commands


class Keks:

    i_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|streamable.com|redd.i'
                't)\/[^\ ]*(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')
    v_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|youtu.be|youtube.com'
                '|twitch.tv)\/[^\ ]*')

    reddit = praw.Reddit(client_id=secrets.CLIENT_ID,
                         client_secret=secrets.REDDIT_TOKEN,
                         user_agent=secrets.USER_AGENT)

    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()

        self.image_link = re.compile(Keks.i_string)
        self.video_link = re.compile(Keks.v_string)

    def get_link(self):
        self.cur.execute("SELECT url FROM subs WHERE status = 'approved';")
        subreddits = self.cur.fetchall()
        if not subreddits:
            return "Blank"

        subreddit = self.reddit.subreddit(random.choice(subreddits)[0])
        submissions = subreddit.new(limit=5)
        for submission in submissions:
            v_link = self.video_link.match(submission.url)
            i_link = self.image_link.match(submission.url)
            if v_link or i_link:
                return submission.url
            else:
                pass

    @commands.command(pass_context=True)
    async def topkek(self, ctx):

        sender = ctx.message.author

        self.cur.execute("SELECT user_id FROM users WHERE user_id = ?;", (sender.id,))
        row = self.cur.fetchone()

        link = Keks.get_link(self)
        print(link)
        if link == None:
            return
        elif link == "Blank":
            return await self.yeebot.say("There are no subreddits to retrieve the toppest keks from, "
                                         "Please submit subreddits using !addsub <subreddit url>")
        else:
            self.cur.execute("SELECT * FROM links WHERE link = ?;", (link,))
            link_exists = self.cur.fetchone()
            if link_exists:
                return await self.yeebot.say("The current top kek ( " + link + " ) has already been kekked. "
                                             "You will not receive credit.")
            else:
                if row:
                    self.cur.execute("INSERT INTO links (link, status, submitter_id, submitter_name)"
                                     "VALUES (?, 'review', ?, ?);", (link, sender.id, sender.name,))
                    self.cur.execute("COMMIT;")

                    self.cur.execute("UPDATE users SET meme_bucks = meme_bucks + 1 WHERE user_id = ?;", (sender.id,))
                    self.cur.execute("COMMIT;")

                    return await self.yeebot.say(  "Top kek: " + str(link) + " has also been submitted "
                                                   "for review. Here's 1 memebuck for your miniscule time")
                else:
                    self.cur.execute("INSERT INTO links (link, status, submitter_id, submitter_name)"
                                     "VALUES (?, 'review', ?, ?);", (link, sender.id, sender.name,))
                    self.cur.execute("COMMIT;")

                    return await self.yeebot.say( "Top kek: " + str(link) + " You are not registered for memebucks,"
                                                  " and therefore will not be eligible for credit.")

    @commands.command(pass_context=False)
    async def addsub(self, *args):

        self.cur.execute("SELECT url FROM subs WHERE url = ?;", (args[0],))
        row = self.cur.fetchone()

        if row:
            return await self.yeebot.say("This subreddit has already been submitted.")
        else:
            self.cur.execute("INSERT INTO subs (url, status) VALUES (?, 'review');", (args[0],))
            self.cur.execute("COMMIT;")

            return await self.yeebot.say("Subreddit submitted for review")

    @commands.command(pass_context=False)
    async def subreview(self, amount=1):

        if not amount:
            return await self.yeebot.say('Please use the format `!subreview'
                                         ' <1-5>`')
        if amount < 1 or amount > 5:
            return await self.yeebot.say('Please use the format `!subreview'
                                             ' <1-5>`')
        elif amount >= 1 and amount <= 5:
            self.cur.execute("SELECT url FROM subs WHERE status = 'review' LIMIT ?;", (amount,))

            subs_to_approve = self.cur.fetchall()
            if not subs_to_approve:
                return await self.yeebot.say("There are no pending sub reviews")
            else:
                num = 1
                for row in subs_to_approve:
                    await self.yeebot.say('{}: Sub {} is pending review'.format(num, row[0]))
                    num += 1

    @commands.command(pass_context=False)
    async def subapprove(self, sub=1):

        if not sub:
            return await self.yeebot.say('Please use the format `!subapprove'
                                         ' <1-5>`')

        if sub < 1 or sub > 5:
            return await self.yeebot.say('Please use the format `!subapprove'
                                             ' <1-5>`')
        elif sub >= 1 and sub <= 5:
            self.cur.execute("SELECT url FROM subs WHERE status = 'review';")

            subs_to_approve = self.cur.fetchall()
            if not subs_to_approve:
                return await self.yeebot.say("There are no pending sub reviews")
            else:
                row = subs_to_approve[sub - 1]
                self.cur.execute("UPDATE subs SET status = 'approved' WHERE url = ?;", (row[0],))
                self.cur.execute("COMMIT;")

                return await self.yeebot.say("Sub {} has been approved.".format(row[0],))

def setup(yeebot):
    yeebot.add_cog(Keks(yeebot))