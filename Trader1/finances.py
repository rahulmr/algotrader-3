from bittrex import Bittrex

class Finances:

    def getTotalAmount(self):
        my_bittrex = Bittrex('####', '####')
        btc_balance = my_bittrex.get_balance('BTC')['result']['Balance']
        return float(btc_balance)

    def getBuyAmount(self):
        my_bittrex = Bittrex('###', '###')
        btc_balance = my_bittrex.get_balance('BTC')['result']['Balance']
        return (btc_balance/5)
