import csv
from dateutil import parser
from twython import Twython

OAUTH_API_KEY = "[Please supply oauth API key]"
OAUTH_API_SECRET = "[Please supply oauth API secret]"
OAUTH_CONSUMER_KEY = "[Please supply oauth consumer key]"
OAUTH_CONSUMER_SECRET = "[Please supply oauth consumer secret]"

# Ask the user to input a station name
print "Enter station name"
station_name = raw_input()

with open('tubestops.csv') as f:

    # Get a list of station coords
    # We store these along with the desired search radius for convenience
    # when querying to the twitter API
    rows = csv.reader(f)
    stations = {}
    for name, _, _, lat, lng, zone, pc in rows:
        stations[name] = [lat, lng, '1mi']

    # Initialize the twitter api
    twitter = Twython(OAUTH_API_KEY, OAUTH_API_SECRET,
                      OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)

    # Fetch 100 tweets for the user's chosen station
    geo = stations[station_name]
    data = twitter.search(q='drunk', geocode=','.join(geo), count=100)

    # Find the time difference between first and last tweet
    # - this gives us a drunken tweet rate for that station
    tweets = data['statuses']
    last_ts = parser.parse(tweets[0]['created_at'])
    first_ts = parser.parse(tweets[-1]['created_at'])
    interval = (last_ts - first_ts).seconds
    rate = (len(tweets) * 1.0) / interval

    print "{} is {} drunk".format(station_name, rate)
