import urllib
import simplejson as json
from twython import Twython

#twitter initialisation

API_KEY = 'BoP0mE4gtGZlh1me29lug'
API_SECRET = 'xteLnU2uu3KEKxZx8hc1wfPic0gs5JvosmRP9VBA6c'
ACCESS_TOKEN = '2417467056-2aZr2bQSGaDcRnbqR7QAHC95TXXSPbyQr2jONYa'
ACCESS_TOKEN_SECRET = 'LBKmR3OXxVFiLEM9zeiYNe0tKwUyiFdfmz27ts36AuhHW'

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#freebase polics retrieval

apiKey = 'AIzaSyD-mnJ5Gff-xJDpEU78Pc5iXLbMHmK4FPA'
url = 'https://www.googleapis.com/freebase/v1/search?'

party = 'republican'

parameters = { 
    'filter': '(all type:politician member_of:' + party + ')',
    'limit': 220,
    'indent': True,
    'spell': 'always',
    'key': apiKey,
    'output' : '(/internet/social_network_user/twitter_id)'
  };

parameters = urllib.urlencode(parameters)

print parameters

# print url
jsonObject = urllib.urlopen(url + parameters).read()
content = json.loads(jsonObject)
content = content['result']

count = 0

for item in content:
	x = item['output']['/internet/social_network_user/twitter_id']
	if x != {}:
            y = x['/internet/social_network_user/twitter_id'][0]
            print y

print count
