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

video_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|youtu.be'
                        '|youtube.com|twitch.tv)\/[^\ ]*')

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

            cur.execute("SELECT link, submitter_name FROM links WHERE status ="
                        " 'approved' ORDER BY RANDOM() LIMIT 1;")

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
                await yeebot.say("Thank you for your submission, {}."
                                 .format(sender.name))

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


@yeebot.command(pass_context=True)
async def review(ctx, amount=1):
    sender = ctx.message.author
    if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:
        
        if amount < 1 or amount > 5:
            return await yeebot.say('Please use the format `!review <1-5>`')
        
        elif amount >= 1 and amount <= 5:
            cur.execute("SELECT link, submitter_name FROM links WHERE status "
                        "= 'review' LIMIT ?;", (amount,))

            links_to_review = cur.fetchall()

            if links_to_review:
                num = 1
                for row in links_to_review:
                    await yeebot.say('{}\) Submitted by: {}, {}'.format(
                                     num, row[1], row[0]))
                    num += 1
            else:
                return await yeebot.say('There are no links to review.')
        else:
            return await yeebot.say('Please use the format `!review <1-5>` '
                                    'to review submitted links')
    
    else:
        pass


@yeebot.command(pass_context=True)
async def approve(ctx, amount='1'):
    sender = ctx.message.author
    if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:
        
        try:
            if int(amount) < 1 or int(amount) > 5:
                return await yeebot.say('Please use the format `!approve <1-5>`')

            elif int(amount) >= 1 and int(amount) <= 5:
                cur.execute("SELECT link, submitter_id FROM links WHERE status="
                            "'review' LIMIT ?;",
                            (amount,))
                
                links_to_approve = cur.fetchall()

                if links_to_approve:
                    num = 1

                    for row in links_to_approve:
                        #grab the submitter for the link
                        submitter = find(lambda m: m.id == row[1],
                                         ctx.message.server.members)

                        #update the row in the links table with approved
                        cur.execute("UPDATE links SET status = 'approved', review"
                                    "er_name = ?, reviewer_id = ? where link = ?;",
                                    (sender.name, str(sender.id),
                                     row[0]))
                        conn.commit()

                        #check if submitter has a row in users table
                        cur.execute("SELECT user_id FROM users WHERE user_id ="
                                    " ?;", (submitter.id,))
                        submitter_row = cur.fetchone()
                        submitter_id = submitter_row[0]
                        
                        # if they do update the user row in the db with new 
                        # balance
                        if submitter_row:
                            cur.execute("UPDATE users SET meme_bucks = meme_bucks"
                                        " + 10 WHERE user_id = ?;", (submitter.id,))
                            conn.commit()

                            cur.execute("SELECT meme_bucks FROM users WHERE user_"
                                        "id = ?;", (submitter.id,))
                            meme_bucks_row = cur.fetchone()
                            meme_bucks = meme_bucks_row[0]

                            await yeebot.send_message(submitter, 'Your lin'
                                         'k was approved. Your balance is now {}.'
                                         ' {}'.format(meme_bucks, row[0]))                    
                        
                        # if they don't, create a row for them
                        else:
                            cur.execute("INSERT INTO users (user_id, username, me"
                                        "me_bucks) VALUES (?, ?, ?);",
                                        (submitter.id, submitter_name, 110))
                            conn.commit()

                            cur.execute("SELECT meme_bucks FROM users WHERE user_"
                                        "id = ?;", (submitter.id,))
                            meme_bucks_row = cur.fetchone()
                            meme_bucks = meme_bucks_row[0]

                            await yeebot.send_message(submitter, 'Your lin'
                                         'k was approved. A Bank of Memerica acco'
                                         'unt was created on your behalf. Your ne'
                                         'w balance is {}.'.format(meme_bucks))
                        
                    return await yeebot.say('{} link(s) approved.'.format(amount))

                else:
                    return await yeebot.say('There are no links awaiting review')
        
        except ValueError:
            # TODO 
            # approve 1 link and give person 10 memebucks
            cur.execute("SELECT link, submitter_id, status FROM links WHERE link = ?"
                        , (amount, ))

            link_row = cur.fetchone()
            
            if link_row:
                
                link_submitter = find(lambda m: m.id == link_row[1],
                                      ctx.message.server.members)

                if link_row[2] == 'rejected' or link_row[2] = 'review':

                    cur.execute("UPDATE links SET status = 'approved' WHERE "
                                "link = ?", (link_row[0],))
                     
                    cur.execute("SELECT meme_bucks FROM users WHERE user_id ="
                                "?;", (link_row[1],)
                    meme_row = cur.fetchone()

                    if meme_row:
                        cur.execute("UPDATE users SET meme_bucks = meme_bucks"
                                    " + 1 WHERE user_id = ?", (link_row[1],))
                        con.commit()
                        cur.execute("SELECT meme_bucks FROM users WHERE"
                                    "user_id = ?;", (link_row[1],))

                        await yeebot.send_message(link_submitter, 'Your link '
                                                  '`{}` has been approved. '
                                                  'Your new balance is {}.'
                                                  .format(link_row[0],
                                                          meme_row[0]))
                    else:          
                        cur.execute("INSERT INTO users (user_id, username, me"
                                    "me_bucks) VALUES (?, ?, ?);",
                                    (submitter.id, submitter_name, 110))
                        conn.commit()
                        await yeebot.send_message(link_submitter, 'Your link '
                                                  '`{}` was approved, and a '
                                                  'Bank of Memerica account '
                                                  'was established on your '
                                                  'behalf. Your new balance '
                                                  'is 110. Happy meming!'


                    return await yeebot.say('`{}` has been approved.'
                                            .format(link_row[0]))
                    
                else:
                    return await yeebot.say('That link is already approved.')

            else:
                return await yeebot.say('That link has not been submitted.')


@yeebot.command(pass_context=True)
async def reject(ctx, amount='1'):

    sender = ctx.message.author 
    
    if ctx.message.channel.id == secrets.REVIEW_CHANNEL_ID:
        try:
            if int(amount) < 1 or int(amount) > 5:
                return await yeebot.say('Please use the format `!reject <1-5|link>`')
            
            elif int(amount) >= 1 and int(amount) <= 5:
                cur.execute("SELECT link, submitter_id FROM links WHERE status = "
                            "'review' LIMIT ?;", (amount,))
                rows = cur.fetchall()
                
                for row in rows:
                    link_submitter = find(lambda m: m.id == row[1],
                                          ctx.message.server.members)
                        
                    cur.execute("UPDATE links SET status = 'rejected' WHERE link =?",
                                (row[0],))
                    conn.commit()
                    await yeebot.send_message(link_submitter, 'Your link {} has been'
                                              ' rejected.')
                
                return await yeebot.say('{} link(s) rejected.'.format(amount))

        except ValueError:
            cur.execute("SELECT link, submitter_id, status FROM links WHERE link = "
                        "?;", (amount,))

            row = cur.fetchone()
            
            if row:

                link_submitter = find(lambda m: m.id == row[1],
                                      ctx.message.server.members)

                if row[2] == 'approved':
                    #take away money, and set to rejected
                    cur.execute("UPDATE links SET status = 'rejected' WHERE link ="
                                " ?", (row[0],))
                    cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?",
                                (row[1],))
                    bucks_row = cur.fetchone()
                    meme_bucks = bucks_row[0]
                    if meme_bucks - 10 < 0:
                        cur.execute("UPDATE users SET meme_bucks = 0 WHERE "
                                    "user_id = ?", (row[1],))
                    else:
                        cur.execute("UPDATE users SET meme_bucks = meme_bucks - 10"
                                    " WHERE user_id = ?", (row[1],))
                    conn.commit()
                    
                    #send message to user with balance and link in question
                    cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?",
                                (row[1],))

                    balance_row = cur.fetchone()
                    balance = balance_row[0]

                    await yeebot.send_message(link_submitter, 'Your link'
                                                     ' {} has been rejected. You'
                                                     'r new balance is {}. Thank'
                                                     's for trying.'
                                                     .format(row[0], balance))

                else:
                    #set to rejected
                    cur.execute("UPDATE links SET status = 'rejected' WHERE link="
                                "?;", (row[0],))
                    #send message to user with link in question
                    await yeebot.send_message(link_submitter, 'Your link '
                                                     '{} has been rejected.'
                                                     .format(row[0]))

                return await yeebot.say('`{}` has been rejected.'.format(row[0]))

            else:
                return await yeebot.say("Link doesn't exist in the database.")
    else:
        pass


yeebot.run(secrets.BOT_TOKEN)
