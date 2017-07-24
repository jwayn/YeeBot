import sqlite3
import discord
import re
from discord.ext import commands
from discord.utils import find
import secrets

i_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|streamable.com|redd.i'
            't)\/[^\ ]*(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')
v_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|youtu.be|youtube.com'
            '|twitch.tv)\/[^\ ]*')
memebuck = '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲'


class Memes:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()

        self.image_link = re.compile(i_string)
        self.video_link = re.compile(v_string)

    @commands.command(pass_context=True,
                      description='Return a random meme')
    async def meme(self, ctx):
        sender = ctx.message.author

        meme_bucks_row = self.cur.execute("SELECT meme_bucks FROM users WHERE "
                                          "user_id = ?;", (sender.id,))
        meme_bucks = self.cur.fetchone()

        if meme_bucks:
            if meme_bucks[0] > 0:
                self.cur.execute("UPDATE users SET meme_bucks = meme_bucks - 1"
                                 " WHERE user_id = ?;", (sender.id,))
                self.cur.execute("UPDATE users SET memes_requested = memes_req"
                                 "uested+ 1 WHERE user_id = ?;", (sender.id,))
                self.conn.commit()
                self.cur.execute("SELECT link, submitter_name FROM links WHERE"
                                 " status ='approved' ORDER BY RANDOM() LIMIT "
                                 "1;")

                row = self.cur.fetchone()
                link = row[0]
                submitter = row[1]

                return await self.yeebot.say(link + "\n Please enjoy this deli"
                                             "cious meme brought to you by `{}"
                                             "`. Thank you for your patronage."
                                             .format(submitter))
            else:
                return await self.yeebot.say("Sorry, you don't have enough mem"
                                             "ebucks to complete this transact"
                                             "ion. Submit some memes with `!ad"
                                             "dmeme <https://link.to.meme/meme"
                                             ">` to get some more!")
        else:
            return await self.yeebot.say('Sorry, you need a bank of mememerica'
                                         ' account to complete this transactio'
                                         'n. Use `!memebucks` to establish an '
                                         'account.')

    @commands.command(pass_context=True)
    async def addmeme(self, ctx, *args):

        sender = ctx.message.author

        if args:
            v_link = self.video_link.match(args[0])
            i_link = self.image_link.match(args[0])

            if v_link or i_link:
                self.cur.execute("SELECT submitter_name, status FROM links WHE"
                                 "RE link = ?;", (args[0],))

                link_exists = self.cur.fetchone()

                if link_exists:

                    submitter = link_exists[0]
                    status = link_exists[1]

                    await self.yeebot.delete_message(ctx.message)
                    return await self.yeebot.say('That link has already been s'
                                                 'ubmitted by `{}`. It is curr'
                                                 'ently in status: `{}`.'
                                                 .format(submitter, status))
                else:
                    self.cur.execute("INSERT INTO links (link, status, submitt"
                                     "er_id,submitter_name) VALUES (?, 'review"
                                     "', ?, ?);",
                                     (args[0], sender.id, sender.name))
                    self.conn.commit()

                    await self.yeebot.delete_message(ctx.message)
                    await self.yeebot.say("Thank you for your submission, {}."
                                          .format(sender.name))

                    self.cur.execute("SELECT count(*) FROM links WHERE status"
                                     " = 'review';")
                    review_count = self.cur.fetchone()

                    if review_count == 1:
                        await self.yeebot.send_message(self.yeebot.get_channel(
                            secrets.REVIEW_CHANNEL_ID),
                            'There is 1 link awaiting review.'
                        )
                    else:
                        await self.yeebot.send_message(self.yeebot.get_channel(
                            secrets.REVIEW_CHANNEL_ID),
                            'There are {} links awaiting review.'
                            .format(review_count[0])
                        )
            else:
                return await self.yeebot.say('Please only submit links from Yo'
                                             'utube, GfyCat, Streamable, Twitc'
                                             'h, Imgur, and Reddit. Only direc'
                                             't image links are accepted. Regu'
                                             'lar video links are ok.')
        else:
            return await self.yeebot.say('Please use the format: `!addmeme htt'
                                         'ps://<link.to.meme/meme>`')

    @commands.command(pass_context=True)
    async def review(self, ctx, amount=1):
        sender = ctx.message.author
        if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:

            if amount < 1 or amount > 5:
                return await self.yeebot.say('Please use the format `!review <'
                                             '1-5>`')

            elif amount >= 1 and amount <= 5:
                self.cur.execute("SELECT link, submitter_name FROM links WHERE"
                                 " status = 'review' LIMIT ?;", (amount,))

                links_to_review = self.cur.fetchall()

                if links_to_review:
                    num = 1
                    for row in links_to_review:
                        await self.yeebot.say('{}\) Submitted by: {}, {}'
                                              .format(num, row[1], row[0]))
                        num += 1
                else:
                    return await self.yeebot.say('No links to review.')
            else:
                return await self.yeebot.say('Please use the format `!review <'
                                             '1-5>` to review submitted links')

        else:
            pass

    @commands.command(pass_context=True)
    async def approve(self, ctx, amount='1'):
        sender = ctx.message.author
        if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:

            try:
                if int(amount) < 1 or int(amount) > 5:
                    return await self.yeebot.say('Please use the format `!appr'
                                                 'ove <1-5>`')

                elif int(amount) >= 1 and int(amount) <= 5:
                    self.cur.execute("SELECT link, submitter_id FROM links WHE"
                                     "RE status='review' LIMIT ?;", (amount,))

                    links_to_approve = self.cur.fetchall()

                    if links_to_approve:
                        num = 1

                        for row in links_to_approve:
                            # grab the submitter for the link
                            submitter = find(lambda m: m.id == row[1],
                                             ctx.message.server.members)

                            # update the row in the links table with approved
                            self.cur.execute("UPDATE links SET status = 'appro"
                                             "ved', reviewer_name = ?, reviewe"
                                             "r_id = ? where link = ?;",
                                             (sender.name, str(sender.id),
                                              row[0]))
                            self.conn.commit()

                            # check if submitter has a row in users table
                            self.cur.execute("SELECT user_id FROM users WHERE "
                                             "user_id = ?;", (submitter.id,))
                            submitter_row = self.cur.fetchone()
                            submitter_id = submitter_row[0]

                            # if they do update the user row in the db with new
                            # balance
                            if submitter_row:
                                self.cur.execute("UPDATE users SET meme_bucks "
                                                 "= meme_bucks + 10 WHERE user"
                                                 "_id = ?;", (submitter.id,))
                                self.conn.commit()

                                self.cur.execute("SELECT meme_bucks FROM users"
                                                 " WHERE user_id = ?;",
                                                 (submitter.id,))

                                meme_bucks_row = self.cur.fetchone()
                                meme_bucks = meme_bucks_row[0]

                                await self.yeebot.send_message(submitter,
                                                               'Your link was '
                                                               'approved. Your'
                                                               ' balance is no'
                                                               'w {}. {}'
                                                               .format(
                                                                   meme_bucks,
                                                                   row[0])
                                                               )

                            # if they don't, create a row for them
                            else:
                                self.cur.execute("INSERT INTO users (user_id, "
                                                 "username, meme_bucks) VALUES"
                                                 " (?, ?, ?);",
                                                 (submitter.id, ctx.submitter_name,
                                                  110)
                                                 )
                                self.conn.commit()

                                self.cur.execute("SELECT meme_bucks FROM users"
                                                 " WHERE user_id = ?;",
                                                 (submitter.id,))

                                meme_bucks_row = self.cur.fetchone()
                                meme_bucks = meme_bucks_row[0]

                                await self.yeebot.send_message(submitter,
                                                               'Your link was '
                                                               'approved. A Ba'
                                                               'nk of Memerica'
                                                               ' account was c'
                                                               'reated on your'
                                                               ' behalf. Your '
                                                               'new balance is'
                                                               ' {} {} {}.'
                                                               .format(
                                                                   memebuck,
                                                                   meme_bucks,
                                                                   memebuck)
                                                               )

                        return await self.yeebot.say('{} link(s) approved.'
                                                     .format(amount))

                    else:
                        return await self.yeebot.say('There are no links await'
                                                     'ing review')

            except ValueError:

                self.cur.execute("SELECT link, submitter_id, status FROM links"
                                 " WHERE link = ?", (amount, ))

                link_row = self.cur.fetchone()

                if link_row:

                    link_submitter = find(lambda m: m.id == link_row[1],
                                          ctx.message.server.members)

                    if link_row[2] == 'rejected' or link_row[2] == 'review':

                        self.cur.execute("UPDATE links SET status = 'approved'"
                                         " WHERE link = ?", (link_row[0],))

                        self.cur.execute("SELECT meme_bucks FROM users WHERE user_i"
                                    "d = ?;", (link_row[1],))
                        meme_row = self.cur.fetchone()

                        if meme_row:
                            self.cur.execute("UPDATE users SET meme_bucks = me"
                                             "me_bucks + 1 WHERE user_id = ?",
                                             (link_row[1],))
                            self.con.commit()

                            self.cur.execute("SELECT meme_bucks FROM users WHE"
                                             "RE user_id = ?;", (link_row[1],))

                            await self.yeebot.send_message(link_submitter,
                                                           'Your link `{}` has'
                                                           ' been approved. Yo'
                                                           'ur new balance is '
                                                           '{}.'
                                                           .format(link_row[0],
                                                                   meme_row[0]
                                                                   ))
                        else:
                            self.cur.execute("INSERT INTO users (user_id, user"
                                             "name, meme_bucks) VALUES (?, ?, "
                                             "?);",
                                             (ctx.submitter.id,
                                              ctx.submitter_name,
                                              110))
                            self.conn.commit()
                            await self.yeebot.send_message(link_submitter,
                                                           'Your link `{}` was'
                                                           ' approved, and a B'
                                                           'ank of Memerica ac'
                                                           'count was establis'
                                                           'hed on your behalf'
                                                           '. Your new balance'
                                                           ' is {} 110 {}. Hap'
                                                           'py meming!'
                                                           .format(link_row[0],
                                                                   memebuck,
                                                                   memebuck))

                        return await self.yeebot.say('`{}` has been approved.'
                                                     .format(link_row[0]))

                    else:
                        return await self.yeebot.say('That link is already app'
                                                     'roved.')

                else:
                    return await self.yeebot.say("Link hasn't been submitted.")

    @commands.command(pass_context=True)
    async def reject(self, ctx, amount='1'):

        sender = ctx.message.author

        if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:
            try:
                if int(amount) < 1 or int(amount) > 5:
                    return await self.yeebot.say('Please use the format `!reje'
                                                 'ct <1-5|link>`')

                elif 1 <= int(amount) <= 5:
                    self.cur.execute("SELECT link, submitter_id FROM links WHE"
                                     "RE status = 'review' LIMIT ?;",
                                     (amount,))
                    rows = self.cur.fetchall()

                    for row in rows:
                        link_submitter = find(lambda m: m.id == row[1],
                                              ctx.message.server.members)

                        self.cur.execute("UPDATE links SET status = 'rejected'"
                                         " WHERE link =?", (row[0],))
                        self.conn.commit()
                        await self.yeebot.send_message(link_submitter,
                                                       'Your link {} has been '
                                                       'rejected.'
                                                       .format(row[0]))

                    return await self.yeebot.say('{} link(s) rejected.'
                                                 .format(amount))

            except ValueError:
                self.cur.execute("SELECT link, submitter_id, status FROM links"
                                 " WHERE link = ?;", (amount,))

                row = self.cur.fetchone()

                if row:

                    link_submitter = find(lambda m: m.id == row[1],
                                          ctx.message.server.members)

                    if row[2] == 'approved':
                        # take away money, and set to rejected
                        self.cur.execute("UPDATE links SET status = 'rejected'"
                                         " WHERE link = ?", (row[0],))
                        self.cur.execute("SELECT meme_bucks FROM users WHERE u"
                                         "ser_id = ?", (row[1],))
                        bucks_row = self.cur.fetchone()
                        meme_bucks = bucks_row[0]
                        if meme_bucks - 10 < 0:
                            self.cur.execute("UPDATE users SET meme_bucks = 0 "
                                             "WHERE user_id = ?", (row[1],))
                        else:
                            self.cur.execute("UPDATE users SET meme_bucks = me"
                                             "me_bucks - 10 WHERE user_id = ?",
                                             (row[1],))
                        self.conn.commit()

                        # send message to user with balance
                        # and link in question
                        self.cur.execute("SELECT meme_bucks FROM users WHERE u"
                                         "ser_id = ?", (row[1],))

                        balance_row = self.cur.fetchone()
                        balance = balance_row[0]

                        await self.yeebot.send_message(link_submitter,
                                                       'Your link {} has been '
                                                       'rejected. Your new bal'
                                                       'ance is {}. Thanks for'
                                                       ' trying.'
                                                       .format(row[0],
                                                               balance))

                    else:
                        # set to rejected
                        self.cur.execute("UPDATE links SET status = 'rejected'"
                                         " WHERE link=?;", (row[0],))
                        # send message to user with link in question
                        await self.yeebot.send_message(link_submitter,
                                                       'Your link {} has been '
                                                       'rejected. Thanks for t'
                                                       'rying.'
                                                       .format(row[0]))

                    return await self.yeebot.say('`{}` has been rejected.'
                                                 .format(row[0]))

                else:
                    return await self.yeebot.say("That link doesn't exist in t"
                                                 "he database.")
        else:
            pass


def setup(yeebot):
    yeebot.add_cog(Memes(yeebot))
