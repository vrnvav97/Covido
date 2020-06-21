import requests
import tweepy
import nltk , sys
# nltk.download('vader_lexicon')
from . import credentials
from nltk.sentiment.vader import SentimentIntensityAnalyzer



class APIService:
    _districtDaily = None
    _lastUpadated = 'None'
    _tweets = None
    _sentimentData = []
    sid = None
    def __init__(self):
        APIService.sid = SentimentIntensityAnalyzer()
        print('[INFO] APIService instance Created.')
        print('[INFO] Setting cofiguration for streaming tweets.')
        # self.listener = MaxListener(100)
        auth = tweepy.OAuthHandler(consumer_key=credentials.consumerkey, consumer_secret=credentials.consumersecret)
        auth.set_access_token(credentials.accesstoken, credentials.accesstokensecret)
        self.api = tweepy.API(auth)
        # self.stream = MaxStream(auth, self.listener)
        print('[INFO]  Cofiguration Done!')
 
    def get_district_daily_covid_data(self):
        url = 'https://api.covid19india.org/districts_daily.json'
        r = requests.get(url)
        district_daily = r.json()['districtsDaily']
        APIService._lastUpadated = r.headers['Last-Modified']
        print('[INFO] Got {y} states/UTs data.'.format(y = len(district_daily)))
        print('[INFO] Call Success!')
        APIService._districtDaily = district_daily

    def get_tweets(self, searchTerm = ['covid19', 'Covid', 'Corona'], noofterms = 200, location = 'India'):  
        def analyzeSentiment(Tweets):
            neg, neu, pos, com = 0, 0, 0, 0
            rt_neg, rt_pos, fav_neg, fav_pos = 0, 0, 0, 0
            count = noofterms
            print('[INFO] Calculating polarity of received tweets.')
            for tweet in Tweets:
                a = self.sid.polarity_scores(tweet['Tweet Text'])
                neg += a['neg']
                neu += a['neu']
                pos += a['pos']
                if a['neg'] >= 0.25:
                    rt_neg += tweet['Retweet Count']
                    fav_neg += tweet['Favorite Count']
                if a['pos'] >= 0.25:
                    rt_pos += tweet['Retweet Count']
                    fav_pos += tweet['Favorite Count']
            com = pos-neg
            APIService._sentimentData = {'NEGATIVE' : str(round(neg/count, 3)),
                    'NEUTRAL' : str(round(neu/count, 3)),
                    'POSITIVE' : str(round(pos/count, 3)),
                    'TOTAL' : str(round(com/count, 3))}
            print('[INFO] Done.')
        
        print('[INFO] Start Fetching Tweets related to \n'+ str(searchTerm) +'\n at location '+ location)
        tweets = tweepy.Cursor(self.api.search, q='\"{}\" -filter:retweets'.format(searchTerm), location = 'INDIA', lang = 'en').items(noofterms)
        tweet_list = []
        print('[INFO] Fetch Complete.', sys.getsizeof(tweets))
        for tweet in tweets:        # Fetching Revelent data from the Tweets.
            dict_ = { 
            'Screen Name': tweet.user.screen_name,
                'User Name': tweet.user.name,
                'Tweet Created At': tweet.created_at,
                'Tweet Text': tweet.text,
                'Retweet Count': tweet.retweet_count,
                'Phone Type': tweet.source,
                'Favorite Count': tweet.favorite_count,
                'User Location': tweet.user.location,
                'Tweet Coordinates': tweet.coordinates
            }
            tweet_list.append(dict_)
        analyzeSentiment(tweet_list)
        APIService._tweets = tweet_list
        print(tweet_list)

    def getCovidCount(self, pin):
        obj = {'District': None, 'Country': None, 'State': None, 'Covid_Count': None}
        url = 'https://api.postalpincode.in/pincode/{PINCODE}'.format(PINCODE = pin)
        r = requests.get(url).json()
        obj['status'], obj['Message'], obj['Areas'] = r[0]['Status'], r[0]['Message'], r[0]['PostOffice']
        if obj['status'] == 'Success':
            obj['District'] = r[0]['PostOffice'][0]['District']
            obj['Country'] = r[0]['PostOffice'][0]['Country']
            obj['State'] = r[0]['PostOffice'][0]['State']
            obj['Covid_Count'] = self._districtDaily[obj['State']][obj['District']]
        return obj