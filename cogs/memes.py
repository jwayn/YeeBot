import sqlite3
import discord
import re
from discord.ext import commands
from discord.utils import find
import secrets
from bank import Bank
from bank import Meme

bank = Bank()
memedb = Meme()

i_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|redd.i'
            't)\/[^\ ]*(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')
v_string = ('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|streamable.com'
            '|youtu.be|youtube.com|twitch.tv)\/[^\ ]*')
memebuck = '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲'
THUMBS_UP = "\U0001F44D"
THUMBS_DOWN = "\U0001F44E"

def account_exists(ctx):
    return bank.check_if_exists(ctx.message.author.id)

class Memes:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()

        self.image_link = re.compile(i_string)
        self.video_link = re.compile(v_string)

    @commands.check(account_exists)
    @commands.group(pass_context=True, description='Return a random meme. Cost: 1 memebuck.')
    async def meme(self, ctx):
        if ctx.invoked_subcommand is None:
            if bank.check_balance(ctx.message.author.id) > 1:
                bank.withdraw(ctx.message.author.id, 1)
                returned_meme = memedb.retrieve(user=ctx.message.author)
                return await self.yeebot.say('{} Please enjoy this delicious meme brought to you by {}'.format(returned_meme[0], returned_meme[1]))
            else:
                return await self.yeebot.say("You don't have enough memebucks to do that.")


    @commands.check(account_exists)
    @meme.command(pass_context=True, description="Submit a meme to be reviewed and potentially added to the database.")
    async def add(self, ctx, link):
        if link:
            v_link = self.video_link.match(link)
            i_link = self.image_link.match(link)
            vote_count = 0
            neg_vote = 0
            pos_vote = 0
            if v_link or i_link:
                if memedb.retrieve(link=link):
                    await self.yeebot.delete_message(ctx.message)
                    return await self.yeebot.say("Sorry, that link is already in the database.")
                else:
                    # Add the link to the database, status = review
                    memedb.add(ctx.message.author, link)
                    # delete the submission message
                    await self.yeebot.delete_message(ctx.message)
                    # post the image for voting
                    msg = await self.yeebot.send_message(ctx.message.channel, 'Please vote on the following meme: {}'.format(link))
                    # add thumbs up and thumbs down to the image
                    await self.yeebot.add_reaction(msg, THUMBS_UP)
                    await self.yeebot.add_reaction(msg, THUMBS_DOWN)
                    # wait for votes on the image
                    while vote_count < secrets.VOTES_TO_COMPLETE:
                        reaction = await self.yeebot.wait_for_reaction(message=msg, emoji=[THUMBS_UP, THUMBS_DOWN])
                        print('Reaction added for {}'.format(link))

                        if reaction.reaction.emoji == THUMBS_UP and reaction.user != msg.author:
                            
                            self.cur.execute("SELECT vote FROM votes WHERE voter_id = ? AND link = ?;", (reaction.user.id, link))
                            row = self.cur.fetchone()
                            if row:
                                user_vote = row[0]
                            
                                if user_vote:
                                    if user_vote == 'NEG':
                                        print('User already has an active vote. Removing emoji and updating row.')
                                        await self.yeebot.remove_reaction(msg, THUMBS_DOWN, reaction.user)
                                        self.cur.execute("UPDATE votes SET vote = 'POS' WHERE voter_id = ? AND link = ?;", (reaction.user.id, link))
                                        self.conn.commit()
                                        pos_vote += 1
                                        neg_vote -= 1
                                        print('Positive vote: {}'.format(pos_vote))
                                        print('Negative vote: {}'.format(neg_vote))
                                    else:
                                        print('User already made a positive vote. Do nothing.')
                            else:
                                pos_vote += 1
                                vote_count += 1
                                self.cur.execute("INSERT INTO votes (link, voter_id, vote) VALUES(?, ?, 'POS');", (link, reaction.user.id))
                                self.conn.commit()
                                print('Positive vote: {}'.format(pos_vote))
                                print('Negative vote: {}'.format(neg_vote))


                        elif reaction.reaction.emoji == THUMBS_DOWN and reaction.user != msg.author:
                            self.cur.execute("SELECT vote FROM votes WHERE voter_id = ? AND link = ?;", (reaction.user.id, link))
                            row = self.cur.fetchone()
                            if row:
                                user_vote = row[0]
                                if user_vote:
                                    if user_vote == 'POS':
                                        print('User has an active vote. Removing emoji and updating row')
                                        await self.yeebot.remove_reaction(msg, THUMBS_UP, reaction.user)
                                        self.cur.execute("UPDATE votes SET vote = 'NEG' WHERE voter_id = ? AND link = ?;", (reaction.user.id, link))
                                        self.conn.commit()
                                        pos_vote -= 1
                                        neg_vote += 1
                                        print('Positive vote: {}'.format(pos_vote))
                                        print('Negative vote: {}'.format(neg_vote))
                                    else:
                                        print('User already made a negative vote. Do nothing.')
                            else:
                                neg_vote += 1
                                vote_count += 1
                                self.cur.execute("INSERT INTO votes (link, voter_id, vote) VALUES(?, ?, 'NEG');", (link, reaction.user.id))
                                self.conn.commit()
                                print('Positive vote: {}'.format(pos_vote))
                                print('Negative vote: {}'.format(neg_vote))

                    print('{} vote over'.format(link))
                    if pos_vote > neg_vote:
                        memedb.approve(link)
                        bank.deposit(ctx.message.author.id, 10)
                        await self.yeebot.delete_message(msg)
                        return await self.yeebot.say("{}'s link `{}` has been approved.".format(ctx.message.author.mention, link))
                        
                    elif neg_vote > pos_vote:
                        memedb.reject(link)
                        await self.yeebot.delete_message(msg)
                        return await self.yeebot.say("{}'s link `{}` has been rejected.".format(ctx.message.author.mention, link))
            else:
                await self.yeebot.delete_message(ctx.message)
                return await self.yeebot.say('Please only submit links from Youtube, GfyCat, Streamable, Twitch, Imgur, and Reddit. Only direct image links are accepted. Regular video links are ok.') 

def setup(yeebot):
    yeebot.add_cog(Memes(yeebot))
