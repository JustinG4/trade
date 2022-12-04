import yfinance as yf
from finviz.screener import Screener
from dateutil.parser import *
from datetime import date
import pandas as pd
import pandas_ta as ta
from prettytable import PrettyTable


class OptionHolder:

    def __init__(self):
        self.Ticker = ""
        self.Strike = 0.0
        self.Expiry = None
        self.YahooString = ""
        self.IsCall = False

        self.BidPrice = 0.0
        self.AskPrice = 0.0
        self.FilledPrice = 0.0
        self.FilledAmount = 0.0
        self.CurrentSpread = 0.0
        self.Volume = 0
        self.OpenInterest = 0
        self.PercentChange = 0.0
        self.IV = 0.0
        self.VWAP = 0.0

        self.IdealBuy = 0.0
        self.IdealSell = 0.0

        self.BBandHigh = 0.0
        self.BBandLow = 0.0
        self.RSI = 0.0
        self.SMA = 0.0
        self.BuyScore = 0

        self.HistoricData = None


def get_stock_list(amount_to_return=5):
    filters = ['cap_small', 'geo_usa', 'sh_avgvol_o300', 'sh_opt_option',
               ]

    stock_list = Screener(filters=filters, table='Overview',
                          order='-change')  # Get the performance table and sort it by price ascending

    stockList = []
    for x in stock_list:
        stockList.append(x['Ticker'])

    return stockList[:amount_to_return]


def get_eligible_option_data_for_stock(stock=""):
    stockTicker = yf.Ticker(stock)

    optionHolderReturn = []

    for x in stockTicker.options:
        expirationTime = parse(x)
        if expirationTime.year > date.today().year:

            for index, row in stockTicker.option_chain(x).calls.iterrows():

                historicData = get_daily_data_for_option(row["contractSymbol"])
                if len(historicData) < 8:
                    continue

                newOptionHolder = OptionHolder()
                newOptionHolder.Ticker = stock
                newOptionHolder.IsCall = True
                newOptionHolder.Expiry = expirationTime
                newOptionHolder.FilledPrice = row["lastPrice"]
                newOptionHolder.BidPrice = row["bid"]
                newOptionHolder.AskPrice = row["ask"]
                newOptionHolder.Strike = row["strike"]
                newOptionHolder.CurrentSpread = newOptionHolder.AskPrice - newOptionHolder.BidPrice
                newOptionHolder.PercentChange = round(row["change"], 3)
                newOptionHolder.OpenInterest = row["openInterest"]
                newOptionHolder.IV = round(row["impliedVolatility"], 3)
                newOptionHolder.YahooString = row["contractSymbol"]
                newOptionHolder.HistoricData = historicData
                optionHolderReturn.append(newOptionHolder)

            for index, row in stockTicker.option_chain(x).puts.iterrows():

                historicData = get_daily_data_for_option(row["contractSymbol"])
                if len(historicData) < 8:
                    continue

                newOptionHolder = OptionHolder()
                newOptionHolder.Ticker = stock
                newOptionHolder.IsCall = False
                newOptionHolder.Expiry = expirationTime
                newOptionHolder.FilledPrice = row["lastPrice"]
                newOptionHolder.BidPrice = row["bid"]
                newOptionHolder.AskPrice = row["ask"]
                newOptionHolder.Strike = row["strike"]
                newOptionHolder.CurrentSpread = newOptionHolder.AskPrice - newOptionHolder.BidPrice
                newOptionHolder.PercentChange = round(row["change"], 3)
                newOptionHolder.OpenInterest = row["openInterest"]
                newOptionHolder.IV = round(row["impliedVolatility"], 3)
                newOptionHolder.YahooString = row["contractSymbol"]
                newOptionHolder.HistoricData = historicData
                optionHolderReturn.append(newOptionHolder)

    return optionHolderReturn


def get_daily_data_for_option(option=""):
    stockTicker = yf.Ticker(option)

    # return stockTicker.history(period="1mo", interval="1d", debug=False)
    return stockTicker.history(period="5d", interval="1m", debug=False)


def get_ideal_buy_sell_magic(option):
    option.IdealBuy = round(option.BidPrice + (option.CurrentSpread * .2), 3)
    option.IdealSell = round(option.AskPrice - (option.CurrentSpread * .2), 3)


if __name__ == '__main__':

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    stockList = get_stock_list(5)

    eligibleOptions = []
    for x in stockList:
        print("Checking if stock is eligible: " + x)
        eligibleOptions.extend(get_eligible_option_data_for_stock(x))

    if len(eligibleOptions) == 0:
        print("No data to use")
    else:

        for option in eligibleOptions:
            option.HistoricData["SMA"] = ta.sma(option.HistoricData["Close"], 5)
            option.HistoricData["RSI"] = ta.rsi(option.HistoricData["Close"], 5)
            option.HistoricData["VWAP"] = ta.vwap(low=option.HistoricData["Low"],
                                                  high=option.HistoricData["High"],
                                                  close=option.HistoricData["Close"],
                                                  volume=option.HistoricData["Volume"])
            bbandData = ta.bbands(option.HistoricData["Close"], 5, 2)
            option.HistoricData["BBU"] = bbandData["BBU_5_2.0"]
            option.HistoricData["BBL"] = bbandData["BBL_5_2.0"]

            option.BBandHigh = round(option.HistoricData["BBU"][-1], 3)
            option.BBandLow = round(option.HistoricData["BBL"][-1], 3)
            option.RSI = round(option.HistoricData["RSI"][-1], 3)
            option.SMA = round(option.HistoricData["SMA"][-1], 3)
            option.VWAP = round(option.HistoricData["VWAP"][-1], 3)
            option.Volume = round(option.HistoricData["Volume"].sum(), 3)
            option.CurrentSpread = round(
                max(option.HistoricData["Close"][-5:]) - min(option.HistoricData["Close"][-5:]), 3)
            get_ideal_buy_sell_magic(option)

        for option in eligibleOptions:
            if option.RSI <= 40:
                option.BuyScore = option.BuyScore + 1
            if option.Volume >= 100:
                option.BuyScore = option.BuyScore + 1
            if option.HistoricData["Close"][-1] <= option.BBandLow:
                option.BuyScore = option.BuyScore + 1
            if option.SMA <= option.VWAP:
                option.BuyScore = option.BuyScore + 1
            if option.CurrentSpread >= 0.05:
                option.BuyScore = option.BuyScore + 1
            if option.FilledPrice == option.BidPrice:
                option.BuyScore = option.BuyScore + 1
            if option.IV <= 40:
                option.BuyScore = option.BuyScore + 1
            if option.PercentChange <= 0:
                option.BuyScore = option.BuyScore + 1

        outputTable = PrettyTable()

        outputTable.field_names = ["Sr. no.", "Ticker", "Strike", "Expiry", "Bid", "Filled", "Ask", "Ideal (Buy/Sell)",
                                   "Spread", "Vol / OI", "BB (S/R)", "RSI", "VWAP", "SMA(5)", "Today Gain", "IV",
                                   "B-Score"]

        outputTable.align["Sr. no."] = "c"
        outputTable.align["Ticker"] = "c"
        outputTable.align["Strike"] = "c"
        outputTable.align["Expiry"] = "c"
        outputTable.align["Bid"] = "c"
        outputTable.align["Filled"] = "c"
        outputTable.align["Ask"] = "c"
        outputTable.align["Ideal (Buy/Sell)"] = "c"
        outputTable.align["Spread"] = "c"
        outputTable.align["Vol / OI"] = "c"
        outputTable.align["BB (S/R)"] = "c"
        outputTable.align["RSI"] = "c"
        outputTable.align["VWAP"] = "c"
        outputTable.align["SMA(5)"] = "c"
        outputTable.align["Today Gain"] = "c"
        outputTable.align["IV"] = "c"
        outputTable.align["B-Score"] = "c"

        # Sort this shit somehow
        eligibleOptions.sort(key=lambda x: x.BuyScore, reverse=True)

        for index, option in enumerate(eligibleOptions):
            outputTable.add_row(
                [index,
                 option.Ticker,
                 option.Strike,
                 option.Expiry,
                 '{:.3f}'.format(option.BidPrice),
                 '{:.3f}'.format(option.FilledPrice),
                 '{:.3f}'.format(option.AskPrice),
                 '{:.3f}'.format(option.IdealBuy) + " / " + '{:.3f}'.format(option.IdealSell),
                 '{:.3f}'.format(round(option.CurrentSpread, 3)),
                 str(option.Volume) + " / " + str(option.OpenInterest),
                 '{:.3f}'.format(option.BBandLow) + " / " + '{:.3f}'.format(option.BBandHigh),
                 '{:.3f}'.format(option.RSI),
                 '{:.3f}'.format(option.VWAP),
                 '{:.3f}'.format(option.SMA),
                 '{:.3f}'.format(option.PercentChange),
                 option.IV, str(option.BuyScore) + " / 8"])

        print(outputTable)