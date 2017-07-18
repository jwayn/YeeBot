import discord
from discord.ext.commands import Bot
from discord.utils import find
import random
import sqlite3
import re
import secrets
import cogs

image_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:imgur.com|'
                        'streamable.com|redd.it)\/[^\ ]*'
                        '(?:.gif|.gifv|.png|.jpg|.jpeg|.mp4|.apng|.tiff)$')

video_link = re.compile('^(?:http:\/\/|https:\/\/).*\.?(?:gfycat.com|youtu.be'
                        '|youtube.com|twitch.tv)\/[^\ ]*')

conn = sqlite3.connect('db/yee.db')
cur = conn.cursor()

yeebot = Bot(command_prefix='!')
startup_extensions = ['cogs.stats', 'cogs.raffle', 'cogs.misc', 'cogs.memes', 'cogs.memebucks']

@yeebot.event
async def on_ready():
    print('Client logged in.')
    print(yeebot.user.name)
    print(yeebot.user.id)
    print('-----')
    await yeebot.change_presence(game=discord.Game(name="Memes"))

    for extension in startup_extensions:
        try:
            yeebot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extensions {}\n {}'.format(extension, exc))



yeebot.run(secrets.BOT_TOKEN)
