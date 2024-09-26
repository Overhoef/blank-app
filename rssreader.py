import pandas as pd
from feedparser import parse

class RSSReader:

    YAHOO_URL = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s=%s&region=US&lang=en-US'
    
    def __init__(self, stock, max_items=5):
        self.news_list_df = pd.DataFrame()
        self.stock = stock
        self.max_items = max_items

    def read_rss(self):
        """
        :return: pandas.DataFrame
        """
        feed = parse(self.YAHOO_URL % self.stock)
        news_list = []
        for i in range(min(self.max_items, len(feed['entries']))):
            news_list.append([
                feed['entries'][i]['title'], 
                feed['entries'][i]['link'], 
                feed['entries'][i]['published'],
                feed['entries'][i]['summary']
            ])
        self.news_list_df = pd.DataFrame(news_list, columns=['title', 'link', 'published','summary'])
        return self.news_list_df
    