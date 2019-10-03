import time
import ast
from bittrex import Bittrex
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt  # To visualize
# import pandas as pd  # To read data
#from sklearn.linear_model import LinearRegression
from urllib.request import urlopen
from datetime import datetime
#import seaborn as sns; sns.set(color_codes=True)
#import pandas as pd
import importlib
import finances

#*******************************************************************************************#
#*******************************************************************************************#
#
# Get user input
#
#*******************************************************************************************#
#*******************************************************************************************#
print("Let's choose your own trading algorithm")
print("Rank on a scale from 1-10 the importance of the following criteria when selecting a coin")
print("The reccommended coin will be displayed based on your preferences")
print("Click any button to continue")
next = input
print("Volatility of coin in recent days (1-10)")
volatility_score = input()
print("Volume increase of coin in recent days (1-10)")
volume_score = input()
print("Price deviation from recent days (1-10)")
deviation_score = input()




my_bittrex = Bittrex('******',
                     '####')

#*******************************************************************************************#
#*******************************************************************************************#
#
# Open tracer coins, open ledger list, open profit list
#
#*******************************************************************************************#
#*******************************************************************************************#
tracer_coins = []

f = open('ledger.txt', 'r+')
ledger_text = f.read()
ledger_list = ast.literal_eval(ledger_text)

t = open('tracer.txt', 'r+')
tracer_text = t.read()
tracer = ast.literal_eval(tracer_text)
for value in tracer:
    tracer_coins = value['coin']

p = open('profits.txt', 'r+')
profits = float(p.read())


#*******************************************************************************************#
#*******************************************************************************************#
#
# Buy coin
#
#*******************************************************************************************#
#*******************************************************************************************#

def buyCoin(coin):
    my_bittrex = Bittrex('******',
                         '00b08625bdfc4c979af2e39b4179b4d9')
    market = 'BTC-' + coin
    price_btc = my_bittrex.get_ticker(market)['result']['Ask']
    finance = finances.Finances()
    size = (finance.getBuyAmount() / price_btc)
    #size = ((profits*0.92)/(price_btc))
    my_bittrex.buy_limit(market, size, price_btc)
    print('BOUGHT', coin)
    ledger_list.append({'coin': coin, 'price': price_btc, 'size': size})
    print(ledger_list)
    f = open('ledger.txt', 'w+')
    f.write(str(ledger_list))
    # updateProfitsSpent(profits*0.92)
    f.close()

#*******************************************************************************************#
#*******************************************************************************************#
#
# Return a reccommended coin to buy based off predictor, predictor updates every 6 minutes
# Traces coins that show steep downward trend, buys on first sign of reversal
#
#*******************************************************************************************#
#*******************************************************************************************#


def getPredictions():
    f = open('predictor.txt', 'r+')
    x = f.read()
    y = ast.literal_eval(x)
    p = open('profits.txt', 'r+')
    profits = float(p.read())
    new_data = []
    for z in y:
        my_bittrex = Bittrex('******',
                             '00b08625bdfc4c979af2e39b4179b4d9')
        market = "BTC-" + z['coin']
        price_btc = my_bittrex.get_ticker(market)['result']['Ask']
        new_prices = z['data']['prices']
        new_prices.pop(0)
        new_prices.append(price_btc)

        if z['data']['tracing'] == True:
            if ((price_btc / new_prices[4]) + (new_prices[4] / new_prices[3])) / 2 >= 1:
                finace = finances.Finances()
                amount = finace.getBuyAmount()
                #trader = trader.Trader()
                # trader.buyCoin(z['coin'])
                print('BUY,', z['coin'])
                buyCoin(z['coin'])

        # for i in range(1,len(new_prices)-3):
        #   running_average = running_average + (new_prices[i]/new_prices[i-1]
        #print("% 5s   .......  % 4.3f" % (z['coin'],running_average))
        running_average = ((new_prices[1] / new_prices[0]) + (new_prices[2] / new_prices[1]) + (
            new_prices[1] / new_prices[0]) + (new_prices[3] / new_prices[2])) / 4
        #print("% 5s   .......  % 4.3f" % (z['coin'], running_average))

        new_price_length = len(new_prices)
        if ((price_btc / new_prices[new_price_length - 2]) + (new_prices[new_price_length - 2] / new_prices[new_price_length - 3])) / 2 > 1:
            tracing_bool = False
        elif (running_average) < 0.995:
            print("STARTED TRACING", z['coin'])
            tracing_bool = True
        else:
            tracing_bool = False

        data = {
            'coin': z['coin'],
            'data': {
                'prices': new_prices,
                'slope': new_prices[1] / new_prices[0],
                'tracing': tracing_bool
            }



        }
        new_data.append(data)
    # print(new_data)
    f = open('predictor.txt', 'w+')
    f.write(str(new_data))
    f.close()


#*******************************************************************************************#
#*******************************************************************************************#
#
# Return a reccommended coin to buy w/o input from predictor, daily "good" bet
#
#*******************************************************************************************#
#*******************************************************************************************#
def updateBuyingScore():
    my_bittrex = Bittrex('******',
                         '00b08625bdfc4c979af2e39b4179b4d9')

    my_markets = ['BTC-ETH', 'BTC-XRP', 'BTC-RVN', 'BTC-BSV', 'BTC-ADA', 'BTC-LTC', 'BTC-BCH', 'BTC-TRX', 'BTC-XMR',
                  'BTC-SPND', 'BTC-XLM', 'BTC-TUSD', 'BTC-ZEC', 'BTC-NEO', 'BTC-XEM', 'BTC-SOLVE', 'BTC-BAT', 'BTC-DGB', 'BTC-XVG', ]
    prev_day_dict = {}
    volatity_dict = {}
    volume_dict = {}

    for market in my_markets:
        ask = price_btc = my_bittrex.get_ticker(market)['result']['Ask']
        prev_day_dict.update(
            {market: (ask / my_bittrex.get_market_summary(market)['result'][0]['PrevDay'])})
        prev_day_ascending = sorted(
            prev_day_dict, key=prev_day_dict.get, reverse=False)

        volume_dict.update(
            {market: (my_bittrex.get_market_summary(market)['result'][0]['Volume'])})
        volume_ascending = sorted(
            volume_dict, key=volume_dict.get, reverse=True)

        volatity_dict.update({market: (my_bittrex.get_market_summary(market)[
                             'result'][0]['High']) / (my_bittrex.get_market_summary(market)['result'][0]['Low'])})
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
    for market in my_markets:
        score_dict.update({market: (new_prev_dict.get(
            market) + new_volume_dict.get(market) + new_volatility_dict.get(market))})
    sorted_score = sorted(score_dict, key=score_dict.get, reverse=False)
    print("THE SCORE DICT", sorted_score)
    for x in list(sorted_score)[0:1]:
        print("Buy", x)
        return x


#*******************************************************************************************#
#*******************************************************************************************#
#
# Removes a given coin from the ledger
#
#*******************************************************************************************#
#*******************************************************************************************#
def removeFromLedger(price):
    my_bittrex = Bittrex('******',
                         '00b08625bdfc4c979af2e39b4179b4d9')

    new_ledger_list = ledger_list[:] = [
        d for d in ledger_list if d.get('price') != price]
    f = open('ledger.txt', 'w')
    f.write(str(new_ledger_list))


#*******************************************************************************************#
#*******************************************************************************************#
#
# Updates tracer file with coins that match the 3% threshold
#
#*******************************************************************************************#
#*******************************************************************************************#
def updateTracer(coin, price, size):
    my_bittrex = Bittrex('******',
                         '00b08625bdfc4c979af2e39b4179b4d9')

    x = {'coin': coin, 'price': price, 'size': size}
    # print(x)
    list_x = [x]
    t = open('tracer.txt', 'w')
    t.write(str(list_x))
    t.close()


#*******************************************************************************************#
#*******************************************************************************************#
#
# Updates profits after selling a coin
#
#*******************************************************************************************#
#*******************************************************************************************#
def updateProfits(coin, price, size):
    for value in ledger_list:
        if value['coin'] == coin:
            profits = ((price * size) - (value['price'] * size))


#*******************************************************************************************#
#*******************************************************************************************#
#
# Updates profits after buying coin
#
#*******************************************************************************************#
#*******************************************************************************************#
def updateProfitsSpent(amount):
    p = open('profits.txt', 'r')
    profits = float(p.read())
    profits = amount
    p = open('profits.txt', 'w+')
    p.write(str(profits))


#*******************************************************************************************#
#*******************************************************************************************#
#
# Check coin to send to tracer or stoploss
#
#*******************************************************************************************#
#*******************************************************************************************#
def checkCoin(coin, price, size):
    my_bittrex = Bittrex('******',
                         '00b08625bdfc4c979af2e39b4179b4d9')

    market = 'BTC-' + coin
    price_btc = my_bittrex.get_ticker(market)['result']['Ask']
    change = float(price_btc) / float(price)
    print("% 5s   .......  % 4.2f" % (coin, ((change - 1) * 100)), '%')
    # changes.append(change)
    # changes_times.append(int(time.time()))
    #data = pd.DataFrame({'changes': changes ,'changes_times':changes_times})
    #sns.lmplot(x="changes_times", y="changes", hue="changes", data=data)
    if change >= 1.0125:
        my_bittrex.sell_limit(market, size, price_btc)
        # updateTracer(coin,price_btc,size)
        #print("STARTED TRACING ", market)
        removeFromLedger(price)
        print("SOLD ", coin)
    elif change <= 0.99:
        my_bittrex.sell_limit(market, size, price_btc)
        print("SOLD AT STOPLOSS ", market)
        removeFromLedger(price)


#*******************************************************************************************#
#*******************************************************************************************#
#
# Checks trace file... decides to sell coin
#
#*******************************************************************************************#
#*******************************************************************************************#
def trace(coin, size, price):
    market = 'BTC-' + coin
    price_btc = my_bittrex.get_ticker(market)['result']['Ask']
    for x in tracer:
        if (price_btc < price):
            my_bittrex.sell_limit(market, size, price_btc)
            new_tracer_list = tracer[:] = [
                d for d in tracer if d.get('coin') != coin]
            t = open('tracer.txt', 'w')
            t.write(str(new_tracer_list))
            t.close()
            # .updateProfits(coin,price_btc,size)
            removeFromLedger(price)
            print("SOLD COIN", coin)
        else:
            updateTracer(coin, price, size)
            print("KEEP TRACING", coin)
            #print("CURRENT GAIN", (price_btc/x['price']))




#*******************************************************************************************#
#*******************************************************************************************#
#
# Reopen ledger
#
#*******************************************************************************************#
#*******************************************************************************************#
f = open('ledger.txt', 'r+')
ledger_text = f.read()
ledger_list = ast.literal_eval(ledger_text)


my_markets_data = ['ETH', 'XRP', 'RVN', 'BSV', 'ADA', 'LTC', 'BCH', 'TRX', 'XMR',
                   'SPND', 'XLM', 'TUSD', 'ZEC', 'NEO', 'XEM', 'SOLVE', 'BAT', 'DGB', 'XVG', ]
for market in my_markets_data:
    link = "https://min-api.cryptocompare.com/data/histohour?fsym=" + market + \
        "&tsym=BTC&limit=10&api_key={c9179662969879a869846053d20a99a63c11d86263e47e1b5330630a7b12a895}"
    f = urlopen(link)
    x = f.read()
    y = json.loads(x)
    open_one = y['Data'][0]['open']
    open_two = y['Data'][10]['open']


#*******************************************************************************************#
#*******************************************************************************************#
#
# Repeats every minute... if coin is in Tracer, see if sell, if coin is not in Tracer, send to check
#
#*******************************************************************************************#
#*******************************************************************************************#
changes = []
changes_times = []
tracer_coins = []
finace = finances.Finances()
p = 0
# print(finace.getTotalAmount())
for i in range(600):
    updateProfitsSpent(finace.getTotalAmount())
    for value in ledger_list:
        # print(value['coin'])
        market = 'BTC-' + value['coin']
        price_btc = my_bittrex.get_ticker(market)['result']['Ask']
        #t = open('tracer.txt','r+')
        #tracer_text = t.read()
        #tracer = ast.literal_eval(tracer_text)
        # for value in tracer:
        #    tracer_coins.append(value['coin'])
        #    print(tracer_coins)
        # print(value['coin'])
        # if value['coin'] in tracer_coins:
        #    print("CHECKING TRACE")
        #    trace(value['coin'],value['size'],value['price'])
        # else:
        checkCoin(value['coin'], value['price'], value['size'])
        if p == 5:
            print("--------------------")
            getPredictions()
            time.sleep(5)
            print(datetime.now())


        if p != 5:
            p = p + 1
        else:
            p = 0
    print("--------------------")
    time.sleep(60)


#*******************************************************************************************#
#*******************************************************************************************#
#
# Close files
#
#*******************************************************************************************#
#*******************************************************************************************#

f.close()
t.close()
