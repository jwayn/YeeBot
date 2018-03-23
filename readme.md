# YeeBot
## A bot made with discord.py and love

YeeBot is centralized, and uses a specific channel for reviewing memes that are submitted. For this reason, it is not recommended to invite YeeBot to multiple servers. Instead, it is recommended to run an instance of YeeBot on a cheap VPS such as Digital Ocean.

## TODO:
There is a [Trello Project](https://trello.com/b/70M7ljxB/yeebot) tracking the progress of YeeBot.
* Rework the way images are submitted and voted upon to make it a community effort rather than a dictorial process
* Complete raffle system
* 'Royalties' to a user when an image they submitted is randomly returned by YeeBot
* Actually comment the code
* Add docker section in 'Getting Started'


## Getting Started:
```bash
$ git clone https://github.com/jaspric/YeeBot.git
$ pip install -R requirements
$ vim secrets.py (copy the blurb from below, and fill out your credentials)
$ python bot.py
```
  
* System Requirements:
  * python 3.5 or greater
  
* The secrets.py file in the root directory of YeeBot needs to have the follow information:
```python
BOT_TOKEN = '<bot_token here>'
CLIENT_ID = '<discord client id here>'
CLIENT_SECRET = '<discord client secret here>'

REDDIT_TOKEN = '<reddit token here>'
REDDIT_CLIENT_ID = '<reddit client id here>'
USER_AGENT = '<reddit user agent here>'

REVIEW_CHANNEL_ID = '<channel id for the discord channel you want to dedicate meme reviews to>'
ADMIN_ROLES = ['admin role 1', 'admin role 2', 'admin role 3']
```
