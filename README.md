# twitter-bot
A simple twitter bot to read from a list of tweets and send it to TL hell. 

# Requirements
 * Python3 >= 3.6
 * Twython
 * Twitter API tokens https://stackoverflow.com/questions/1808855/getting-new-twitter-api-consumer-and-secret-keys

 # Run 

To do a test run
 ````sh
python3 twitterbot.py --secrets secrets.json --test --tweet
````

To actually send a tweet
 ````sh
python3 twitterbot.py --secrets secrets.json --tweet
````

To get a list of recent tweets from the user
 ````sh
python3 twitterbot.py --secrets secrets.json --dump_list
````
