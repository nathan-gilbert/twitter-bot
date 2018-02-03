#!/usr/bin/python3
# Created By : Nathan Gilbert
""" Twitter Bot for tweeting a message multiple times in order to save time and
spread the message across different times."""

#externals
import os
import sys
import argparse
import datetime
import json
from twython import Twython, TwythonError

#internals
from tweet_manager import TweetManager

if __name__ == "__main__":
    LOG_FILE = 'twitter_bot.log'
    tweet_list = ""
    issue_tweet = False
    dump_list = False
    debug = False
    test_tweet = False
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--tweet_list', dest='tweet_list_file',
                            action='store', help='list of tweets to pull from')
    arg_parser.add_argument('--tweet', dest="issue_tweet", action='store_true',
                            help='send a random tweet from the current saved list')
    arg_parser.add_argument('--dump_list', dest="dump_list",
                            action='store_true',
                            help='dump the current tweets out to a list')
    arg_parser.add_argument('--debug', dest='debug', action='store_true',
                            help='print debugging info')
    arg_parser.add_argument('--test', dest='test_tweet', action='store_true',
                            help='print a test tweet stdout only')
    arg_parser.add_argument('--secrets', dest='secret_file', action='store',
                            help='json file to pull credentials from', default=None)

    if len(sys.argv) < 2:
        arg_parser.print_help()
        sys.exit(0)

    args = vars(arg_parser.parse_args())
    if args["dump_list"]:
        dump_list = True

    if args["issue_tweet"]:
        issue_tweet = True

    if args["tweet_list_file"] != "":
        tweet_list = args["tweet_list_file"]

    if args["debug"]:
        debug = True

    if args["test_tweet"]:
        test_tweet = True

    #change the scripts working directory to the one where it resides
    working_dir = os.path.dirname(sys.argv[0])
    if working_dir != '':
        os.chdir(working_dir)

    # read in the secrets from JSON file
    if args["secret_file"] is not None:
        with open(args["secret_file"], 'r') as secret_file:
            json_creds = json.load(secret_file)
    else:
        print("No credentials supplied. use --secrets <file>.json")

    #private keys and secrets
    consumer_key = json_creds["consumer_key"]
    consumer_secret = json_creds["consumer_secret"]
    access_token_key = json_creds["access_token_key"]
    access_token_secret = json_creds["access_token_secret"]
    account_name = json_creds["account_name"]

    #setup twython
    twitter = Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)

    if debug:
        print(twitter.verify_credentials())

    try:
        #gets the user's twitter feed
        #user_timeline = twitter.get_home_timeline(screen_name=account_name)
        #
        #https://dev.twitter.com/rest/reference/get/statuses/user_timeline
        #user_timeline = twitter.get_user_timeline(screen_name=account_name,
        #                                          count=200,
        #                                          exclude_replies=True,
        #                                          include_rts=False)
        # get the last 200 of the user's tweets
        # use max_id to go further back in a user's timeline
        user_timeline = twitter.get_user_timeline(screen_name=account_name,
                                                  count=200,
                                                  exclude_replies=True,
                                                  include_rts=False)
    except TwythonError as e:
        if debug:
            print(e)

    tm = TweetManager()
    for tweet in user_timeline:
        try:
            if debug:
                print(tweet)
            t = tweet['text'].encode("utf-8")
            tm.add_recent_tweet(t.decode("utf-8"))
        except UnicodeEncodeError as e:
            if debug:
                print(e)

    if dump_list:
        with open('tl_dump.txt', 'w') as outFile:
            for tweet in user_timeline:
                try:
                    t = tweet['text'].encode("utf-8")
                    outFile.write(t.decode("utf-8") + "\n")
                except UnicodeEncodeError as e:
                    continue

    #issue a random tweet from the campaign_tweet list
    #read in the campaign tweets
    if issue_tweet:
        #get a tweet out of the database
        tweet = tm.rando_sqlite_tweet()
        while tm.is_in_last_50_tweet(tweet):
            tweet = tm.rando_sqlite_tweet()

        if test_tweet:
            print(tweet)
        else:
            if debug:
                print(tweet)

            #update status with old tweet
            exception_thrown = False
            exception_msg = ""
            try:
                twitter.update_status(status=tweet)
                #update stats
            except TwythonError as e:
                if debug:
                    print(e.msg)
                exception_thrown = True
                exception_msg = e.msg

            with open(LOG_FILE, 'a') as log_file:
                timestamp = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
                if not exception_thrown:
                    log_file.write(timestamp + " : " + tweet + "\n")
                else:
                    log_file.write(timestamp + " : " + tweet + " error: " +
                                   exception_msg + "\n")
