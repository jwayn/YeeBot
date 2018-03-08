import discord
from discord.ext.commands import Bot
import sqlite3
import re
import os
import errno
import secrets

image_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|'
                        'streamable.com|redd.it)\/[^\ ]*'
                        '(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')

video_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|youtu.be'
                        '|youtube.com|twitch.tv)\/[^\ ]*')

try:
    os.makedirs('db')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

conn = sqlite3.connect('db/yee.db')
cur = conn.cursor()

yeebot = Bot(command_prefix='!')
startup_extensions = ['cogs.stats', 'cogs.colors', 'cogs.misc', 'cogs.memes', 'cogs.memebucks'] 

@yeebot.event
async def on_ready():
    print('Client logged in.')
    print(yeebot.user.name)
    print(yeebot.user.id)
    print('-----')

    cur.execute('CREATE TABLE IF NOT EXISTS links(link text, status text, '
                'submitter_id text, submitter_name text, reviewer_id'
                ' text, reviewer_name text);')

    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id TEXT UNIQUE, username '
                'TEXT, meme_bucks INTEGER, memes_submitted INTEGER DEFAULT 0,'
                ' memes_requested INTEGER DEFAULT 0, memes_approved INTEGER '
                'DEFAULT 0, memes_rejected INTEGER DEFAULT 0, PRIMARY KEY(user_id));')

    await yeebot.change_presence(game=discord.Game(name="Memes"))

    for extension in startup_extensions:
        try:
            yeebot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extensions {}\n {}'.format(extension, exc))


yeebot.run(secrets.BOT_TOKEN)
