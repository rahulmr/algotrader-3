import time
import ast
from bittrex import Bittrex
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt  # To visualize
#import pandas as pd  # To read data
#from sklearn.linear_model import LinearRegression
from datetime import datetime
import finances
#import trader

class Predictor:
    def __init__(self):
            #self.bar = 1
        self.run()
    def getPredictions():
        f = open('predictor.txt','r+')
        x = f.read();
        y = ast.literal_eval(x)
        p = open('profits.txt','r+')
        profits = float(p.read())
        new_data = []
        for z in y:
            my_bittrex = Bittrex('535221f7425749ce8b147f70cbf43d19', '00b08625bdfc4c979af2e39b4179b4d9')
            market = "BTC-"+z['coin']
            price_btc = my_bittrex.get_ticker(market)['result']['Ask']
            new_prices = z['data']['prices']
            new_prices.pop(0)
            new_prices.append(price_btc)

            if z['data']['tracing'] == True:
                if ((price_btc/new_prices[4])+(new_prices[4]/new_prices[3]))/2 >= 1:
                    finace = finances.Finances()
                    amount = finace.getBuyAmount()
                    #trader = trader.Trader()
                    #trader.buyCoin(z['coin'])
                    print('BUY,', z['coin'])


            #for i in range(1,len(new_prices)-3):
            #   running_average = running_average + (new_prices[i]/new_prices[i-1]
            #print("% 5s   .......  % 4.3f" % (z['coin'],running_average))
            running_average = ((new_prices[1]/new_prices[0]) + (new_prices[2]/new_prices[1]) + (new_prices[1]/new_prices[0]) + (new_prices[3]/new_prices[2]))/4
            print("% 5s   .......  % 4.3f" % (z['coin'],running_average))

            new_price_length = len(new_prices)
            if ((price_btc/new_prices[new_price_length-2])+(new_prices[new_price_length-2]/new_prices[new_price_length-3]))/2 > 1:
                tracing_bool = False
            elif (running_average) < 0.995:
                print("STARTED TRACING",z['coin'])
                tracing_bool = True
            else:
                tracing_bool = False

            data = {
                'coin': z['coin'],
                'data':{
                    'prices': new_prices,
                    'slope': new_prices[1]/new_prices[0],
                    'tracing': tracing_bool
                }



            }
            new_data.append(data)
        #print(new_data)
        f = open('predictor.txt','w+')
        f.write(str(new_data))
        f.close()


    for i in range(60):
        getPredictions()
        print(datetime.now())
        print("--------------------")
        time.sleep(300)


'''

    eth_market = []
    xrp_market = []
    rvn_market = []
    bsv_market = []
    ada_market = []
    ltc_market = []
    bch_market = []
    trx_market = []
    xmr_market = []
    spnd_market = []
    xlm_market = []
    doge_market = []
    zec_market = []
    neo_market = []
    xem_market = []
    solve_market = []
    bat_market = []
    dgb_market = []
    xvg_market = []
    tusd_market = []

    all_markets_prices = [
            eth_market,xrp_market,rvn_market,bsv_market,ada_market,ltc_market,bch_market,trx_market,xmr_market,spnd_market,
            xlm_market,tusd_market,doge_market,zec_market,neo_market,xem_market,solve_market,bat_market,dgb_market,xvg_market
        ]
    my_markets = ['BTC-ETH','BTC-XRP','BTC-RVN','BTC-BSV','BTC-ADA','BTC-LTC','BTC-BCH','BTC-TRX','BTC-XMR','BTC-SPND','BTC-XLM','BTC-TUSD','BTC-ZEC','BTC-NEO','BTC-XEM','BTC-SOLVE','BTC-BAT','BTC-DGB','BTC-XVG',]
    my_bittrex = Bittrex('535221f7425749ce8b147f70cbf43d19', '00b08625bdfc4c979af2e39b4179b4d9')
    while len(all_markets_prices[0]) < 2:
        i=0
        for market in my_markets:
            price_btc = my_bittrex.get_ticker(market)['result']['Ask']
            all_markets_prices[i].append(price_btc)
            i = i+1
        time.sleep(60)
    for market in all_markets_prices:
        print(market)
        '''
