from bittrex import Bittrex

class Finances:

    def getTotalAmount(self):
        my_bittrex = Bittrex('535221f7425749ce8b147f70cbf43d19', '00b08625bdfc4c979af2e39b4179b4d9')
        btc_balance = my_bittrex.get_balance('BTC')['result']['Balance']
        return float(btc_balance)

    def getBuyAmount(self):
        my_bittrex = Bittrex('535221f7425749ce8b147f70cbf43d19', '00b08625bdfc4c979af2e39b4179b4d9')
        btc_balance = my_bittrex.get_balance('BTC')['result']['Balance']
        return (btc_balance/5)
