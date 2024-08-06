from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='') # api key goes here

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us')

for headline in top_headlines['articles']:
    print(headline['title'])

