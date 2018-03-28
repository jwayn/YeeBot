import sqlite3

class Bank:
    def __init__(self):
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()

    def check_if_exists(self, user_id):
        self.cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?;", (user_id,))
        row = self.cur.fetchone()
        print('User ID is: {}'.format(user_id))
        if row:
            return True
        else:
            return False

    def check_balance(self, user_id):
        self.cur.execute("SELECT meme_bucks FROM users WHERE user_id = ?", (user_id,))
        row = self.cur.fetchone()
        print('Balance checked.')
        return row[0]


    def withdraw(self, user_id, amount):
        self.cur.execute("UPDATE users set meme_bucks = meme_bucks - ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()


    def deposit(self, user_id, amount):
        self.cur.execute("UPDATE users set meme_bucks = meme_bucks + ? WHERE user_id = ?", (amount, user_id))
        self.conn.commit()


    def transfer(self, from_user, to_user, amount):
        self.withdraw(from_user, amount)
        self.deposit(to_user, amount)
        print('Memebucks transferred.')
        self.conn.commit()


class Meme:
    def __init__(self):
        self.conn = sqlite3.connect('db/yee.db')
        self.cur = self.conn.cursor()


    def add(self, user, link):
        self.cur.execute("INSERT INTO links (link, status, submitter_id, submitter_name) VALUES (?, 'REVIEW', ?, ?)", (link, user.id, user.name))
        self.conn.commit()


    def approve(self, link):
        self.cur.execute("UPDATE links SET status = 'APPROVED' WHERE link = ?;", (link,))
        self.conn.commit()


    def reject(self, link):
        self.cur.execute("UPDATE links SET status = 'REJECTED' WHERE link = ?;", (link,))
        self.conn.commit()


    def retrieve(self, user=None, link=None):

        if link:
            self.cur.execute("SELECT link FROM links WHERE link = ?;", (link,))
            row = self.cur.fetchone()

            if row:
                return True
            else:
                return False

        else:
            self.cur.execute("UPDATE users SET meme_bucks = meme_bucks - 1, memes_requested = memes_requested + 1 WHERE user_id = ?;", (user.id,))
            self.conn.commit()
            self.cur.execute("SELECT link, submitter_name FROM links WHERE status = 'APPROVED' ORDER BY RANDOM() LIMIT 1;")
            row = self.cur.fetchone()
            return [row[0], row[1]]

