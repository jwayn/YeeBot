import sqlite3
import links
import uuid

conn = sqlite3.connect("yee.db")
cur = conn.cursor()

amount = 5

cur.execute("SELECT link FROM links WHERE status = 'approved' LIMIT ?", (amount, ))
links = cur.fetchall()

for link in links:
    for l in link:
        print(l)
