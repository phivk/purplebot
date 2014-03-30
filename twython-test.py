from twython import Twython

API_KEY = 'BoP0mE4gtGZlh1me29lug'
API_SECRET = 'xteLnU2uu3KEKxZx8hc1wfPic0gs5JvosmRP9VBA6c'
ACCESS_TOKEN = '2417467056-2aZr2bQSGaDcRnbqR7QAHC95TXXSPbyQr2jONYa'
ACCESS_TOKEN_SECRET = 'LBKmR3OXxVFiLEM9zeiYNe0tKwUyiFdfmz27ts36AuhHW'

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

twitter.update_status(status="Purple bot says hello world!")