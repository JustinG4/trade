import cbpro
import time
from datetime import datetime
import websocket
import json
import ccxt
import config
import schedule
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from slack import WebClient
from termcolor import colored
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


key = 'e262108f66dbb4f0839dee8f75476639'
b64secret = 'XUY9tWRDCKnjYoifihN9wgq4St8EKYDzbdtIliktREiEmxV7jvdEUNaQHdSd9xkLAnF01GbV+0/xP+gykNozJw=='
passphrase = 'wharthog'

debug = False

public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
#auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase, "https://api-public.sandbox.pro.coinbase.com")


# @brief gets account holdings
def isHolding(ticker):
    key = 'dd640fb5ccd38e5158ded79d903cfd0f'
    b64secret = '5bAW4oj1ezmr+wWEjPtoT48zpY3HgM6uICGqin8SDE9Xf9E3f3f+S+9oA3icab3xh0KpM/RNBd232oE1hiwzhg=='
    passphrase = 'wharthog2'

    debug = False
    ac = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    hodl = {}
    accounts = ac.get_accounts()

    for account in accounts:
        hodl[account['currency']] = account['hold']

    if float(hodl.get(ticker)) > 0:
        return True
    else:
        return False


# @brief gets account holdings
def getHoldings():
    # c694f49e-339e-4151-a8dd-f03a927c3172 is USD
    account = auth_client.get_account('c694f49e-339e-4151-a8dd-f03a927c3172')
    balance = float(account['available'])

    return balance

# @brief gets price of ticker
def getPrice(ticker):
    payload = public_client.get_product_ticker(ticker)

    try:
        price = float(payload['price'])
    except KeyError:
        price = 9

    #print('getPrice::' + str(price))
    return price

# @brief gets profit
def getProfit(price, amt, tgtprice):
    # take in price of coin
    # take in amount being purchased

    # get amount of crypto
    camt = amt / price

    # get target price

    # calculate profit
    profit = (camt * tgtprice) - (camt * price)

    print(colored('Current projected profit from sale: $' + str(profit), 'blue'))

    return profit

# @brief executes limit buy
def buy(price, amt, ticker):
    # Limit order-specific method
    auth_client.place_limit_order(product_id=ticker,
                                  side='buy',
                                  price=price,
                                  size=amt)

# @brief executes limit sell
def sell(price, amt, product_id):
    # Sell 0.01 BTC @ 200 USD
    auth_client.sell(price=price,
                     size=amt,
                     order_type='limit',
                     product_id=product_id)

# @brief automatically trades jasmy
def ThirtyAday(limit_price):
    # init
    buy = False
    sell = False
    f = open("/Users/justingreenfield/Desktop/transactions.txt", "w")

    # get amount of coin
    accounts = auth_client.get_accounts()
    for x in range(0, len(accounts)):
        holding = float(accounts[x]['hold'])
        if holding > 0:
            amt = holding
            sell = True
        else:
            amt = 400
            buy = True

    # if no coins buy
    if buy:
        price = getPrice('JASMY_USD')
        buytime = datetime.now()
        if (price - limit_price) <= 0.002:
            buy(limit_price, amt, 'JASMY_USD')
            f.write('Bought - at ' + str(buytime))
            print('Bought - at ' + str(buytime))
        else:
            f.write('Not buying - at ' + str(buytime))
            print('Not buying - at ' + str(buytime))
        f.write('Price: ' + str(price))
        print('Price: ' + str(price))

    # get valuation
    valuation = price * amt
    f.write('Valuation: $' + str(valuation) + '\n')
    print('Valuation: $' + str(valuation) + '\n')

    if sell:
        selltime = datetime.now()
        price = getPrice()
        if (price - limit_price) > 0.01:
            # sell(price, amt, 'JASMY_USD')
            f.write('Sold - at ' + str(selltime))
            print('Sold - at ' + str(selltime))
        else:
            f.write('Not selling - at ' + str(selltime))
            print('Not selling - at ' + str(selltime))
        f.write('Price: ' + str(price))
        print('Price: ' + str(price))

    f.close()

# @brief returns cryptos under $bound
def getCryptos(bound):
    cryptos = {}
    elements = public_client.get_products()
    for element in elements:
        ticker = element['base_currency'] + '-USD'
        price = getPrice(ticker)
        ticker = element['base_currency'] + '/USD'

        if price < bound:
            cryptos[ticker] = price
            print(ticker, price)
    return cryptos

# @brief gets interesting cryptos that might be ... profitable
def getVolatileCryptos(ticker, duration, bound):
    binance = ccxt.coinbasepro()
    deltas = []
    trading_pair = ticker
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    i = 0

    candles = binance.fetch_ohlcv(trading_pair, duration)

    for candle in candles:
        time = datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
        dates.append(time)
        open_data.append(candle[1])
        print(candle[1])
        high_data.append(candle[2])
        print(candle[2])
        low_data.append(candle[3])
        print(candle[3])
        close_data.append(candle[4])
        print(candle[4])

    for x in range (1, len(low_data)):
        delta = high_data[x] - low_data[x]
        if debug: print('getVolatileCryptos::' + str(delta))
        deltas.append(delta)
        print(delta, deltas)

        if delta > bound:
            i += 1
            # fig = go.Figure(data=[go.Candlestick(x=dates,
            #                                      open=open_data, high=high_data,
            #                                      low=low_data, close=close_data)])
            #fig.show()

    avg = sum(deltas) / len(deltas)
    if debug: print('getVolatileCryptos::' + str(avg))

    if i / len(low_data) > 0.3 or avg > bound:
        return ticker
    else:
        ticker = ''
        return ticker

# @brief class for getting live data
class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        if msg_type == 'ticker':
            time_val = msg.get('time', ('-' * 27))
            price_val = msg.get('price', None)
            if price_val is not None:
                price_val = float(price_val)
            product_id = msg.get('product_id', None)

            print(f"{time_val:30} \
                        {price_val:.3f} \
                        {product_id}\tchannel type:{msg_type}")

    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")


# @brief send slack msg
def send(msg):
    #SLACK_API_TOKEN = 'xoxe.xoxp-1-Mi0yLTI3MTkwODczNzcwNjEtMjczNDY3NjIwMjgzMy0yNzA3Mzk4OTY2ODIzLTI3MTUzMzc2MjE3OTgtN2ZmNWY2ZmVhYzk1MWE5MTcxMDliYjg5YzAzMDgxZjJjNjcwMTkzODdkZDY5ZTU2NjZjODRjZDlkZWJlZGYwNQ'
    SLACK_API_TOKEN = 'xoxb-2719087377061-2722274523570-3xON3308DXqxkJ3LEOkHFqIY'
    slack = WebClient(SLACK_API_TOKEN)
    slack.chat_postMessage(
        channel='#testdev4',
        text=msg)
    #assert response["message"]["text"] == "Hello world!"


# @brief animates the graph
def animate(i):

    plt.axis([0, 10, 0, 1])

    for i in range(10):
        y = np.random.random()
        plt.scatter(i, y)
        plt.pause(0.05)

    plt.show()


def dothisshit(input_price):
    url = 'https://ftx.us/markets'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options, executable_path=ChromeDriverManager().install())
    driver.get(url)

    symbols = {}
    tickers = driver.find_elements_by_css_selector('tr')
    price = 0.0
    name = ''
    for ticker in tickers:
        words = (ticker.text).split()

        if '/USDT' in words[0]:
            name = words[0]
            price = float(words[-2].replace(',', ''))

            if price < input_price:
                symbols[name] = price

    print(symbols)
    print(list(symbols.keys()))
    return symbols


#dothisshit(5.00)