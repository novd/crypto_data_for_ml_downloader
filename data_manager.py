import requests
import json
import warnings
import matplotlib.pyplot as plt

# api website : https://www.cryptocompare.com/cryptopian/api-keys

api_key = "asdasdw124tgsd5_top_secret_api_key_324908712klsafjiae"


def get_historical_data(type, cryptocurrency_symbol="BTC", real_currency_symbol="USD", limit=100, time_stamp_limit=None):

    limit_for_recursion = limit - 2000

    if limit > 2000:
        limit = 2000

    elif limit <= 0:
        warnings.warn("Limit is outside the scope")
        return []

    if time_stamp_limit is not None:
        time_stamp_limit = "&toTs=" + str(time_stamp_limit)
    else:
        time_stamp_limit = ""

    historical_url = "https://min-api.cryptocompare.com/data/"+type+"?fsym=" + cryptocurrency_symbol \
                           + "&tsym=" + real_currency_symbol \
                           + "&limit=" + str(limit) + time_stamp_limit

    page = requests.get(historical_url + "&api_key=" + api_key)
    json_page = json.loads(str(page.content.decode("utf-8")))

    data = [element for element in json_page["Data"]]

    if limit_for_recursion > 0:
        recursion_data = get_historical_data(type, cryptocurrency_symbol, real_currency_symbol, limit_for_recursion, data[0]['time'])
        recursion_data += data
        return recursion_data
    else:
        return data


def create_plot(data, filename, show_plot=False):
    price_array = [element['close'] for element in data]
    date_array = [element['time'] for element in data]

    plt.plot(date_array, price_array, label="Price plot")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig(filename)
    if show_plot:
        plt.show()


def save_data_to_file(data, filename, blockinfo):
    file = open(filename, 'a')
    file.write("\n\n ==============================  " + blockinfo + "  ==============================\n")
    for element in data:
        file.write(str(element) + "\n")



