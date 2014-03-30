import urllib
import simplejson as json
from twitter import *

apiKey = 'AIzaSyD-mnJ5Gff-xJDpEU78Pc5iXLbMHmK4FPA'
url = 'https://www.googleapis.com/freebase/v1/search?'

party = 'democratic'
party = 'republican'


# parameters = { 
#     'filter': '(all type:/government/politician member_of:' + party + ')',
#     'limit': 200,
#     'indent': True,
#     'spell': 'always',
#     'key': apiKey,
#     'output' : '(/internet/social_network_user/twitter_id)'
#   };

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
   		print x
   		count = count + 1

print count