import discord
from discord.ext.commands import Bot
from discord.utils import find
import random
import sqlite3
import re
import secrets

image_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|'
                        'streamable.com|redd.it)\/[^\ ]*'
                        '(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')

video_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat|youtu.be|'
                        'youtube.com|twitch.tv)\/[^\ ]*')

conn = sqlite3.connect('db/yee.db')
cur = conn.cursor()

yeebot = Bot(command_prefix='!')

@yeebot.event
async def on_ready():
    print('Client logged in.')
    print(yeebot.user.name)
    print(yeebot.user.id)
    print('-----')
    await yeebot.change_presence(game=discord.Game(name="Memes"))


@yeebot.command(pass_context=True)
async def meme(ctx, *args):
    sender = ctx.message.author
    cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?", (sender.id,))
    sender_bucks = cur.fetchone()

    if sender_bucks:
        if sender_bucks[0] > 0:

            cur.execute("UPDATE users SET meme_bucks = meme_bucks - 1 WHERE"
                        " user_id = ?;", (sender.id,))
            cur.execute("UPDATE users SET memes_requested = memes_requested"
                        " + 1 WHERE user_id = ?;", (sender.id,))
            conn.commit()

            cur.execute("SELECT link, submitter_name FROM links WHERE status = "
                        "'approved' ORDER BY RANDOM() LIMIT 1;")
            
            row = cur.fetchone()
            link = row[0]
            submitter = row[1]
            
            return await yeebot.say(link + "\n Please enjoy this delicious "
                                    "meme brought to you by '{}'. Thank you "
                                    "for your patronage.".format(submitter))

        else:
            return await yeebot.say("Sorry, you don't have enough memebucks t"
                                    "o complete this transaction. Submit some"
                                    " memes to get some more!")
    else:
        return await yeebot.say('Sorry, you need a bank of mememerica account'
                                ' to complete this transaction. Use `!memebuc'
                                'ks` to establish an account.')


@yeebot.command(pass_context=True)
async def addmeme(ctx, *args):

    sender = ctx.message.author

    if args:
        v_link = video_link.match(args[0])
        i_link = image_link.match(args[0])

        if v_link or i_link:
            cur.execute("SELECT submitter_name, status FROM links WHERE link"
                        " = ?;", (args[0],))

            link_exists = cur.fetchone()

            if link_exists:

                submitter = link_exists[0]
                status = link_exists[1]

                await yeebot.delete_message(ctx.message)
                return await yeebot.say('That link has already been submitted'
                                        ' by `{}`. It is currently in status:'
                                        ' `{}`.'.format(submitter, status))
            else:
                cur.execute("INSERT INTO links (link, status, submitter_id,"
                            " submitter_name) VALUES (?, 'review', ?, ?);",
                            (args[0], sender.id, sender.name))
                cur.execute("UPDATE users SET memes_submitted = memes_submi"
                            "tted + 1 WHERE user_id = ?;", (sender.id,))
                conn.commit()

                await yeebot.delete_message(ctx.message)
                await yeebot.say("Thank you for your submission.")

                cur.execute("SELECT count(*) FROM links WHERE status = 'revie"
                            "w';")
                review_count = cur.fetchone()
                
                if review_count == 1:
                    await yeebot.send_message(yeebot.get_channel(
                          secrets.REVIEW_CHANNEL_ID), 'There is 1 link awaitin'
                          'g review.')
                else:
                    await yeebot.send_message(yeebot.get_channel(
                          secrets.REVIEW_CHANNEL_ID), 'There are {} links awai'
                          'ting review.'.format(review_count[0]))
        else:
            return await yeebot.say('Please only submit links from Youtube, '
                                    'GfyCat, Streamable, Twitch, Imgur, and '
                                    'Reddit. Only direct image links are acc'
                                    'epted. Regular video links are ok.')
    else:
        return await yeebot.say('Please use the format: `!addmeme https://<l'
                                'ink.to.meme/meme>`')

yeebot.run(secrets.BOT_TOKEN)

