#!/usr/bin/python3
# Created By : Nathan Gilbert
""" This module will take in a list of tweets that need to be retweeted """

import random
import sqlite3
from datetime import datetime

class TweetManager:
    """Tweet Manager class """
    def __init__(self):
        # these are the tweets that should be promoted over a period of time
        self._focus_tweet_list = []
        # these are the most recent tweets and should be retweeted randomly
        self._most_recent_tweet_list = []
        self.sqlite_name = "tweet_list.sqlite"

    def init_sqlite_db(self):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE tweet_list (id integer PRIMARY KEY AUTOINCREMENT, msg text, tweet_count integer,
                  last_tweeted text, stop_date text)''')
        conn.commit()
        conn.close()

    def insert_sqlite_tweet(self, msg, stop_date=""):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute('''INSERT INTO tweet_list(msg, tweet_count, last_tweeted, stop_date)
                  VALUES ('{0}', 0, '', '{1}')'''.format(msg, stop_date))
        conn.commit()
        conn.close()

    def rando_sqlite_tweet(self):
        #TODO update last tweeted date & count
        pass

    def delete_sqlite_tweet(self, m):
        pass

    def cleanup_sqlite_tweets(self):
        """ delete all tweets that are beyond the stop_data """
        pass

    def add_focus_tweet(self, tweet):
        """ add a tweet to the focus list """
        self._focus_tweet_list.append(tweet)

    def add_recent_tweet(self, tweet):
        """ adds a single tweet to the master list. """
        self._most_recent_tweet_list.append(tweet)

    def rando_recent_tweet(self):
        """returns a random tweet from the current tweet list."""
        random.seed(datetime.now())
        random_index = random.randint(0, len(self._most_recent_tweet_list) - 1)
        return self._most_recent_tweet_list[random_index]

    def rando_focus_tweet(self):
        """returns a random tweet from the list of twist that warrant focus"""
        random.seed(datetime.now())
        random_index = random.randint(0, len(self._focus_tweet_list) - 1)
        return self._focus_tweet_list[random_index]

    def is_last_50_tweet(self, new_tweet):
        """Is the 'new_tweet' one of the last 50 tweets in the TL"""
        return bool(self._most_recent_tweet_list[-50:].count(new_tweet) > 0)

if __name__ == "__main__":
    tm = TweetManager()
    #tm.init_sqlite_db()
    #tm.insert_sqlite_tweet("yellow", "2019")
