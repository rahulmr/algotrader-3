from iexfinance.refdata import get_symbols
from iexfinance.altdata import get_social_sentiment
from iexfinance.stocks import Stock
from iexfinance.stocks import get_market_volume
# import time
# import ast
# from bittrex import Bittrex
# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json
# from collections import OrderedDict
# import numpy as np
# import matplotlib.pyplot as plt  # To visualize
# # import pandas as pd  # To read data
# #from sklearn.linear_model import LinearRegression
# from urllib.request import urlopen
# from datetime import datetime
# #import seaborn as sns; sns.set(color_codes=True)
# #import pandas as pd
# import importlib
# import finances

#print(get_symbols(output_format='pandas', token="###"))

# print(get_symbols(output_format='pandas', token="###"))
token="#####"
listOfStocks = ['XLF','QQQ','VXX','FXI','EWZ','EFA','EEM','SQQQ']

for stock in listOfStocks:
    stockName = Stock(stock,token='####')
    #print(stock,stockName.get_quote())
    # print(stockName.get_previous_day_prices())

def buyingPredictor():
    prev_day_dict = {}
    volatity_dict = {}
    volume_dict = {}

    prev_day_ascending = []
    for stock in listOfStocks:
        stockName = Stock(stock,token=token)
        #print(stock,stockName.get_quote()['latestPrice'])
        price = stockName.get_quote()['latestPrice']
        prev_day_dict.update({stock: (price / stockName.get_previous_day_prices()['open'])})
        prev_day_ascending = sorted(prev_day_dict, key=prev_day_dict.get, reverse=False)

        volume_dict.update(
            {stock: (stockName.get_quote()['iexVolume'])})
        volume_ascending = sorted(
            volume_dict, key=volume_dict.get, reverse=True)

        volatity_dict.update({stock: (stockName.get_previous_day_prices()['high']) / (stockName.get_previous_day_prices()['low'])})
        volatility_ascending = sorted(
            volatity_dict, key=volatity_dict.get, reverse=True)

    #print('PrevDay ', {key: rank for rank, key in enumerate(prev_day_ascending, key=prev_day_ascending.get, reverse=False)})
    #print('Volume ', sorted(volume_ascending, key=volume_ascending.get, reverse=True))
    i = 0
    new_prev_dict = {}
    for key in prev_day_ascending:
        new_prev_dict.update({key: i})
        i = i + 1
    #print("New Previous",new_prev_dict)

    i = 0
    new_volume_dict = {}
    for key in volume_ascending:
        new_volume_dict.update({key: i})
        i = i + 1
    #print("New Volume",new_volume_dict)

    i = 0
    new_volatility_dict = {}
    #print('Volatility ', sorted(volatility_ascending, key=volatility_ascending.get, reverse=True))
    for key in volatility_ascending:
        new_volatility_dict.update({key: i})
        i = i + 1
    #print("New Volatility", new_volatility_dict)

    score_dict = {}
    for stock in listOfStocks:
        score_dict.update({stock: (new_prev_dict.get(
            stock) + new_volume_dict.get(stock) + new_volatility_dict.get(stock))})
    sorted_score = sorted(score_dict, key=score_dict.get, reverse=False)
    print("THE SORTED DICT BASED OFF PREFERENCES", sorted_score)
    for x in list(sorted_score)[0:1]:
        print("Buy", x)
        return x

print(buyingPredictor())
