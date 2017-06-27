import secrets
import sqlite3
from discord.ext.commands import Bot
from discord.utils import find
import discord
import random

review_channel_id = '328980594677776384'
general_channel_id = '329143971693461504'

conn = sqlite3.connect("yee.db")
cur = conn.cursor()

yeebot = Bot(command_prefix="!")

@yeebot.event
async def on_ready():
    print("Client logged in.")
    print(yeebot.user.name)
    print(yeebot.user.id)
    print('-----')
    await yeebot.change_presence(game=discord.Game(name="Memes"))


@yeebot.command()
async def meme(*args):
    cur.execute("SELECT * FROM links WHERE status = 'approved' ORDER BY RANDOM() LIMIT 1;")
    link = cur.fetchone()[0]
    return await yeebot.say(link)


@yeebot.command(pass_context=True)
async def addmeme(ctx, *args, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    if args:
        if 'youtu' in args[0] or 'gfycat' in args[0] or 'imgur' in args[0] or 'streamable' in args[0] or 'redd' in args[0]:
            cur.execute("SELECT status FROM links WHERE link = ?", (args[0],))
            check = cur.fetchone()
            if check is None:
                cur.execute("INSERT INTO links (link, status, submitter, submitter_name) VALUES (?, 'review', ?, ?)", (args[0], member.id, member.name))
                conn.commit()
                cur.execute("SELECT count(*) FROM links WHERE status = 'review'")
                count = cur.fetchone()[0]
                if count == 1:
                    await yeebot.send_message(yeebot.get_channel(review_channel_id), 'There is 1 link awaiting review.'.format(count))
                else:
                    await yeebot.send_message(yeebot.get_channel(review_channel_id), 'There are {} links awaiting review.'.format(count))
                return await yeebot.say("`{}` has been submitted for review.".format(args[0]))
            else:
                return await yeebot.say("Sorry, that link has already been submitted. It is currently in status: `{}`".format(check[0]))
        else:
            return await yeebot.say("Please only submit links from Youtube, gfycat, streamable, or imgur.")
    else:
        return await yeebot.say("Please use the format: `!addmeme https://link.to.meme/meme`")


@yeebot.command(pass_context=True)
async def review(ctx, amount=1, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    if ctx.message.channel.id == review_channel_id:
        if amount < 1 or amount > 5:
            return await yeebot.say("Please use the format `!review <1-5>`.")
        elif amount > 1 and amount < 6:
            cur.execute("SELECT link, submitter_name FROM links WHERE status = 'review' LIMIT ?", (amount, ))
            links = cur.fetchall()
            if links:
                for row in links:
                    await yeebot.say("Submitted by: {}, `{}`".format(row[1], row[0]))
            else:
                return await yeebot.say("No links to review.")
        else:
            cur.execute("SELECT link, submitter_name FROM links WHERE status = 'review' LIMIT ?", (amount, ))
            links = cur.fetchall()
            if links:
                for row in links:
                    await yeebot.say("Submitted by: {}, {}".format(row[1], row[0]))
            else:
                return await yeebot.say("No links to review.")
    else:
        return await yeebot.say("You do not have permission to execute this command.")


@yeebot.command(pass_context=True)
async def approve(ctx, *args, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    if args[0] not in ['1', '2', '3', '4', '5']:
        if ctx.message.channel.id == review_channel_id:
            cur.execute("SELECT link, submitter FROM links WHERE link = ?", (args[0],))
            row = cur.fetchone()
            approved_link = row[0]
            submitter = find(lambda m: m.id == row[1], ctx.message.server.members)
            mention = submitter.mention
            if approved_link:
                cur.execute("UPDATE links SET status = 'approved', reviewer = ?, reviewer_id = ? where link = ?", (member.name, member.id, approved_link))
                conn.commit()
                await yeebot.send_message(yeebot.get_channel(general_channel_id), '{} Your link: `{}` has been approved.'.format(mention, approved_link))
                return await yeebot.say("`{}` has been approved.".format(approved_link))
        else:
            return await yeebot.say("You do not have permission to execute this command.")
    else:
        limiter = int(args[0])
        cur.execute("SELECT count(*) from links where status = 'review'")
        total_review = int(cur.fetchone()[0])
        if int(total_review) < limiter:
            limiter = int(total_review)

        print("limiter = " + str(limiter))

        for x in range(0, limiter):
            cur.execute("SELECT link, submitter FROM links WHERE status = 'review' LIMIT 1")
            row = cur.fetchone()
            approved_link = row[0]
            submitter = find(lambda m: m.id == row[1], ctx.message.server.members)
            print(row)
            print(approved_link)
            print(row[1])
            mention = submitter.mention
            await yeebot.send_message(yeebot.get_channel(general_channel_id), '{} Your link: `{}` has been approved.'.format(mention, approved_link))
            cur.execute("UPDATE links SET status = 'approved', reviewer = ?, reviewer_id = ? where link = ?", (member.name, member.id, approved_link))
            conn.commit()
        return await yeebot.say("{} links have been approved.".format(limiter))


@yeebot.command(pass_context=True)
async def reject(ctx, *args, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    if args[0] not in ['1', '2', '3', '4', '5']:
        if ctx.message.channel.id == review_channel_id:
            cur.execute("SELECT link, submitter FROM links WHERE link = ?", (args[0],))
            row = cur.fetchone()
            rejected_link = row[0]
            submitter = find(lambda m: m.id == row[1], ctx.message.server.members)
            mention = submitter.mention
            if rejected_link:
                cur.execute("UPDATE links SET status = 'rejected', reviewer = ?, reviewer_id = ? where link = ?", (member.id, member.name, rejected_link))
                conn.commit()
                await yeebot.send_message(yeebot.get_channel(general_channel_id), '{} Your link: `{}` has been rejected.'.format(mention, rejected_link))
        else:
            return await yeebot.say("You do not have permission to execute this command.")
    else:
        limiter = int(args[0])
        cur.execute("SELECT count(*) from links where status = 'review'")
        total_review = int(cur.fetchone()[0])
        if int(total_review) < limiter:
            limiter = int(total_review)

        print("limiter = " + str(limiter))

        for x in range(0, limiter):
            cur.execute("SELECT link, submitter FROM links WHERE status = 'review' LIMIT 1")
            row = cur.fetchone()
            approved_link = row[0]
            submitter = find(lambda m: m.id == row[1], ctx.message.server.members)
            print(row)
            print(approved_link)
            print(row[1])
            mention = submitter.mention
            await yeebot.send_message(yeebot.get_channel(general_channel_id), '{} Your link: `{}` has been rejected.'.format(mention, approved_link))
            cur.execute("UPDATE links SET status = 'rejected', reviewer = ?, reviewer_id = ? where link = ?", (member.name, member.id, approved_link))
            conn.commit()
        return await yeebot.say("{} links have been rejected.".format(limiter))


@yeebot.command(pass_context=True)
async def roll(ctx, *args):
    name = ctx.message.author.name
    args = args[0].lower().split('d')
    die = args[1]
    mod = args[0]
    results = []
    if mod:
        if die in ['4', '6', '8', '10', '12', '20', '100']:
            if int(mod) > 1 and int(mod) < 7:
                for x in range(0, int(mod)):
                    this_roll = random.randrange(1, int(die) + 1)
                    results.append(this_roll)
                results_string = ', '.join(str(x) for x in results)
                return await yeebot.say("{} rolled a d{} {} times and got `{}`!".format(name, die, mod, results_string))
            elif int(mod) == 1:
                result = str(random.randrange(1, int(die) + 1))
                return await yeebot.say("{} rolled a d{} and got `{}`!".format(name, die, result))
            else:
                return await yeebot.say("Please use the format: `!roll <1-6>d<4, 6, 8, 10, 12, 20, 100>` eg: `!roll 2d20`")
        else:
            return await yeebot.say("Please use the format: `!roll <1-6>d<4, 6, 8, 10, 12, 20, 100>` eg: `!roll 2d20`")
    else:
        return await yeebot.say("Please use the format: `!roll <1-6>d<4, 6, 8, 10, 12, 20, 100>` eg: `!roll 2d20`")


class Raffle:
    raffle_live = False
    raffle_entries = []

    def __init__(self):
        pass

    def raffle_entry(user):
        Raffle.raffle_entries.append(user)

    def raffle_drawing():
        winner = random.choice(Raffle.raffle_entries)
        Raffle.raffle_entries = []
        return winner


@yeebot.command(pass_context=True)
async def raffle(ctx):
    if Raffle.raffle_live:
        return await yeebot.say("Sorry, there is already a raffle going on right now.")
    else:
        roles = []
        for role in ctx.message.author.roles:
            roles.append(role.name)
        if 'Admins' in roles:
            Raffle.raffle_live = True
            await yeebot.say("{} has started a raffle! Use `!enter` to make your entry!".format(ctx.message.author.name))
        else:
            return await yeebot.say("You don't have permission to do that.")


@yeebot.command(pass_context=True)
async def enter(ctx):
    if Raffle.raffle_live:
        if ctx.message.author in Raffle.raffle_entries:
            return await yeebot.say("You've already entered this raffle!")
        else:
            Raffle.raffle_entry(ctx.message.author)
            return await yeebot.say("Thanks for joining the raffle, {}!".format(ctx.message.author.name))
    else:
        return await yeebot.say("Sorry, there isn't a raffle going on right now.")


@yeebot.command(pass_context=True)
async def entries(ctx):
    if Raffle.raffle_live:
        roles = []
        for role in ctx.message.author.roles:
            roles.append(role.name)
        if 'Admins' in roles:
            entries = []
            for entry in Raffle.raffle_entries:
                entries.append(entry.name)
            entries = ', '.join(entries)
            entry_string = "Current raffle entries: `{}`".format(entries)
            return await yeebot.say(entry_string)
        else:
            return await yeebot.say("You don't have permission to do that.")
    else:
        return await yeebot.say("Sorry, there isn't a raffle going on right now.")


@yeebot.command(pass_context=True)
async def endraffle(ctx):
    if Raffle.raffle_live:
        roles = []
        for role in ctx.message.author.roles:
            roles.append(role.name)
        if 'Admins' in roles:
            if Raffle.raffle_live:
                return await yeebot.say("And the winner of the raffle is...... {}".format(Raffle.raffle_drawing().mention))
            else:
                return await yeebot.say("Sorry, there isn't a raffle going on right now.")
        else:
            return await yeebot.say("You don't have permission to do that.")
    else:
        return await yeebot.say("Sorry, there isn't a raffle going on right now.")


@yeebot.command(pass_context=True)
async def dickstats(*args):
    return await yeebot.say("Is this some kind of sick joke? You want me to keep track of your guys' dicks?")

try:
    yeebot.run(secrets.BOT_TOKEN)

except KeyboardInterrupt:
    exit()
