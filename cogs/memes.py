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
                    while vote_count < 4:
                        reaction = await self.yeebot.wait_for_reaction(message=msg, emoji=[THUMBS_UP, THUMBS_DOWN])
                        print('Reaction added for {}'.format(link))
                        if reaction.reaction.emoji == THUMBS_UP:
                            #check for users reactions already here
                            pos_vote += 1
                            vote_count += 1
                            self.yeebot.say(pos_vote)
                        elif reaction.reaction.emoji == THUMBS_DOWN:
                            neg_vote += 1
                            vote_count += 1
                            self.yeebot.say(neg_vote)
                        remove_reac = await self.yeebot.on_reaction_remove(
                    print('{} vote over'.format(link))
                    if pos_vote > neg_vote:
                        memedb.approve(link)
                        print('{} approved.'.format(link))
                    elif neg_vote > pos_vote:
                        memedb.reject(link)
                        print('{} rejected.'.format(link))
def setup(yeebot):
    yeebot.add_cog(Memes(yeebot))
