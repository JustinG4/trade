import robin_stocks as r
import pandas as pd
import datetime as dt
import numpy as np
import robin_stocks.robinhood as r


def login(username, password):
    login_var = r.login(username, password, "80000")
    print(login_var)


def get_stocks():
    stocks = r.get_top_100()
    tickers = []
    for number in range(len(stocks)):
        for element in stocks[0]:
            if element == "symbol":
                tickers.append(stocks[number][element])
    return tickers


def get_stocks_from_file(file_name):
    with open(file_name) as reader:
        stock_list = reader.readlines()
        for n in range(len(stock_list)):
            stock_list[n] = stock_list[n].strip("\n")
        return stock_list


def filter_stocks_by_price(tickers, price_to_filter):
    tickers_under_price = {}
    for ticker in tickers:
        new_tickers = r.get_quotes(tickers)
        for new_ticker in new_tickers:
            if float(new_ticker["last_trade_price"]) <= price_to_filter:
                local_ticker = new_ticker["symbol"]
                tickers_under_price[local_ticker] = new_ticker["last_trade_price"]
    print(tickers_under_price)
    return tickers_under_price


def delta_probability_strike_price_finder(tickers_under_price, exp_date, call_or_put):
    delta_and_win_percent = {}
    for ticker in tickers_under_price:
        try:
            strike_price = str(round(float(tickers_under_price.get(ticker)), 1))
            while True:
                try:
                    option_data = r.find_options_by_expiration_and_strike(
                        ticker, exp_date, strike_price, call_or_put
                    )
                    if call_or_put == "put":
                        if (float(strike_price) % 0.5) == 0:
                            strike_price = str(round(float(strike_price) - 0.50, 1))
                            if float(option_data[0]["delta"]) >= -0.15:
                                break
                        else:
                            strike_price = str(round(float(strike_price) - 0.10, 1))
                    if call_or_put == "call":
                        if (float(strike_price) % 0.5) == 0:
                            strike_price = str(round(float(strike_price) + 0.50, 1))
                            if float(strike_price) >= float(
                                (5 * float(tickers_under_price.get(ticker)))
                            ):
                                break
                            if float(option_data[0]["delta"]) <= 0.15:
                                break
                        else:
                            strike_price = str(round(float(strike_price) + 0.10, 1))
                except IndexError:
                    if float(strike_price) <= 0.0:
                        break
                    continue
            print(option_data)
            delta_and_win_percent[ticker] = [
                option_data[0]["last_trade_price"],
                option_data[0]["delta"],
                option_data[0]["strike_price"],
                tickers_under_price[ticker],
            ]
        except AttributeError:
            print("could not get options")
        except IndexError:
            print("excluded from screening because price is too high")
    print(delta_and_win_percent)
    return delta_and_win_percent


def print_option_data(delta_and_win_percent):
    for stock in delta_and_win_percent:
        percent_win = round(
            (
                float(delta_and_win_percent[stock][0])
                / float(delta_and_win_percent[stock][3])
            )
            * 100,
            2,
        )
        probability = abs(round(float(delta_and_win_percent[stock][1]) * 100, 2))
        strike = round(float(delta_and_win_percent[stock][2]), 2)
        option_price = round(float(delta_and_win_percent[stock][0]), 2)
        price = round(float(delta_and_win_percent[stock][3]), 2)

        print(
            str(stock)
            + ":  Percent Win - "
            + str(percent_win)
            + "% Probability Lose - "
            + str(probability)
            + "% "
            + " Strike - "
            + str(strike)
            + " Option Price - "
            + str(option_price)
            + " Price - "
            + str(price)
        )


def probeForBuy():

    login('justinrgreenfield@me.com', 'cecxi6-qeqxox-Wojfus')

    list_of_stocks = get_stocks()
    print(list_of_stocks)
    price_to_filter_by = 250.0
    filtered_stocks = filter_stocks_by_price(list_of_stocks, float(price_to_filter_by))

    # # Get today's date
    # today = dt.datetime.today()
    #
    # # Format the date as YYYY-MM-DD
    # formatted_date = today.strftime('%Y-%m-%d')
    #
    # # Add 45 days to the date
    # new_date = today + dt.timedelta(days=45)
    #
    # # Format the new date as YYYY-MM-DD
    # formatted_new_date = new_date.strftime('%Y-%m-%d')
    # strike_to_filter_by = formatted_new_date
    #
    # calls_or_puts = 2
    # options_data = delta_probability_strike_price_finder(
    #     filtered_stocks, strike_to_filter_by, "put"
    # )
    #
    # print_option_data(options_data)

    symbols = filtered_stocks
    for symbol in symbols:
        data = r.options.find_tradable_options_for_stock(symbol, optionType='put')

        df = pd.DataFrame(data)
        df['min_ticks'][0]

        now = dt.datetime.now()
        start = now + dt.timedelta(30)
        end = now + dt.timedelta(45)

        date_generated = [start + dt.timedelta(days=x) for x in range(0, (end-start).days)]
        date_list = []
        for date in date_generated:
            date_list.append(date.strftime("%Y-%m-%d"))

        new_df = df[df['expiration_date'].isin(date_list)].reset_index(drop=True)
        test = new_df.strike_price.unique()

        strike_list = new_df.strike_price.unique().tolist()
        current_price = r.stocks.get_latest_price(symbol)[0]
        strike_list.append(current_price)
        strike_list_sort = sorted(strike_list,key=float)
        expirationDate = sorted(new_df.expiration_date.unique())[-1]
        i = strike_list_sort.index(current_price)
        strike_a = strike_list_sort[i+1] #long call strike price

        data = r.options.find_options_for_stock_by_expiration_and_strike(symbol, expirationDate, strike_a, optionType='call', info=None)
        df2 = pd.DataFrame(data)

        price = df2['low_fill_rate_buy_price'][0]
        # robin_stocks.orders.order_buy_option_limit(price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gfd')
