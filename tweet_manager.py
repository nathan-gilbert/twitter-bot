#!/usr/bin/python3
""" Class for manipulating an sqlite database containing tweets & stats """

import sqlite3
import sys
from datetime import datetime

class TweetManager:
    """Tweet Manager class """
    def __init__(self):
        self._most_recent_tweet_list = []
        self.sqlite_name = "tweet_list.sqlite"

    def init_sqlite_db(self):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE tweet_list (id integer PRIMARY KEY AUTOINCREMENT, msg text,
                  tweet_count integer, last_tweeted text, stop_date text)''')
        conn.commit()
        conn.close()

    def init_sqlite_db_with_tweets(self, tweets):
        self.init_sqlite_db()
        for tweet in tweets:
            print(tweet)
            self.insert_sqlite_tweet(tweet)

    def insert_sqlite_tweet(self, m, stop_date=""):
        m = m.strip()
        if len(m) > 280:
            raise ValueError

        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute("""INSERT INTO tweet_list(msg, tweet_count, last_tweeted, stop_date)
                  VALUES (?, ?, ?, ?)""", (m, 0, "", stop_date))
        conn.commit()
        conn.close()

    def rando_sqlite_tweet(self):
        #get random tweet
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute('''SELECT * FROM tweet_list ORDER BY RANDOM() LIMIT 1;''')
        row = c.fetchone()
        conn.close()
        #update last_tweeted date
        return row[1]

    def update_sqlite_tweet_stats(self, m):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        current_time = str(datetime.now())
        c.execute("SELECT * FROM tweet_list WHERE msg=?", (m,))
        row = c.fetchone()
        c.execute("UPDATE tweet_list SET tweet_count=?, last_tweeted=? WHERE ID=?",
                  (int(row[2])+1, current_time, row[0]))
        conn.commit()
        conn.close()

    def get_all_tweets(self):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute("SELECT * FROM tweet_list")
        rows = c.fetchall()
        conn.close()
        return rows

    def delete_sqlite_tweet(self, m):
        conn = sqlite3.connect(self.sqlite_name)
        c = conn.cursor()
        c.execute("SELECT * FROM tweet_list WHERE msg=?;", (m))
        row = c.fetchone()
        c.execute("DELETE from tweet_list WHERE ID=?", (row[0]))
        conn.commit()
        conn.close()

    def cleanup_sqlite_tweets(self):
        """ delete all tweets that are beyond the stop_data """
        #TODO
        pass

    def add_recent_tweet(self, tweet):
        """ adds a single tweet to the master list. """
        self._most_recent_tweet_list.append(tweet)

    def is_in_last_50_tweet(self, new_tweet):
        """Is the 'new_tweet' one of the last 50 tweets in the TL"""
        return new_tweet in self._most_recent_tweet_list[-50:]

if __name__ == "__main__":
    tm = TweetManager()

    tl = []
    with open(sys.argv[1], 'r') as inFile:
        tl = inFile.readlines()
    #creates new database an adds all tweets from input file
    tm.init_sqlite_db_with_tweets(tl)
    #appends all tweets from input file to current db
    #for t in tl:
    #    tm.insert_sqlite_tweet(t)
