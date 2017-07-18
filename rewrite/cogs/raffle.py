import sqlite3
import discord
from discord.ext import commands


class Raffle:
    def __init__(self, yeebot):
        self.yeebot = yeebot
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()
        self.entries = []
        self.raffle_live = False




def setup(yeebot):
    yeebot.add_cog(Raffle(yeebot))
