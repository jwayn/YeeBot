# YeeBot
## A bot made with discord.py and love

YeeBot is centralized, and uses a specific channel for reviewing memes that are submitted. For this reason, it is not recommended to invite YeeBot to multiple servers, as the memes that are being submitted to the review channel can easily become overwhelming.

Everything is slowly being moved into the rewrite. Once complete, that will become the root directory.

### TODO:
There is a [Trello Project](https://trello.com/b/70M7ljxB/yeebot) tracking the progress of YeeBot.

### Getting Started:
* Clone YeeBot
* PIP requirements:

  * discord.py
  * matplotlib
  * praw
  * numpy
  
* System Requirements:
  * python 3.5 or greater
  
* Create a 'secrets.py' file in the root directory of YeeBot with the following information:
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
* ????
* Profit
