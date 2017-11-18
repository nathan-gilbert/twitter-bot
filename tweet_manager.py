#!/usr/bin/python3
# Created By : Nathan Gilbert
""" This module will take in a list of tweets that need to be retweeted """

import random
from datetime import datetime

class TweetManager:
    """Tweet Manager class """
    def __init__(self):
        # these are the tweets that should be promoted over a period of time
        self._focus_tweet_list = []
        # these are the most recent tweets and should be retweeted randomly
        self._most_recent_tweet_list = []

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
        """Is the 'new_tweet' one of the last 5 tweets that were tweeted."""
        return bool(self._most_recent_tweet_list[-50:].count(new_tweet) > 0)
