import requests
from win10toast import ToastNotifier
import datetime
import time

toaster = ToastNotifier()

url = 'https://rest.coinapi.io/v1/exchangerate/BTC/EUR'
headers = {'X-CoinAPI-Key': 'API_KEY'}
res = requests.get(url, headers=headers)
res = res.json()
act_btc = round(res['rate'], 2)

start_time = time.time()


def get_rounded_per(value):
    if value > act_btc:
        return str(abs(round(100 - (value / act_btc) * 100, 2))) + "%"
    else:
        return str(round(100 - (value / act_btc) * 100, 2)) + "%"


print("\nNotification will appear every 15 minutes...\n")
print("Actual value of BTC:", act_btc, "€")
print("\nSet limits for this session...\n")
min_notify = round(float(input("If BTC will be bellow value (€): ")), 2)
print("This is decrease of:", get_rounded_per(min_notify))
max_notify = float(input("If BTC will be above value (€): "))
print("This is increase of:", get_rounded_per(max_notify), "\n")


def load_state():
    actual_time = datetime.datetime.now()
    btc = 0.00
    response = requests.get(url, headers=headers)
    response = response.json()

    file = open("history/" + datetime.datetime.now().strftime("%d-%m-%Y") + ".txt", "a")

    text_to_write = "Datetime: " + actual_time.strftime("%d-%m-%Y %H:%M:%S") + "\nValue: " + str(response['rate']) \
                    + "\n\n"

    file.write(text_to_write)
    actual_time = actual_time.strftime("%H:%M:%S")

    for key in response:
        if key == "rate":
            btc = round(float(response[key]), 2)
        if key == "time":
            response[key] = actual_time
        print(key, "=", response[key], end="\n")
    print()

    toaster.show_toast("Actual value of BTC - " + actual_time, str(btc) + " €", "btc-logo.ico")

    if btc < min_notify:
        toaster.show_toast("Limit notification", "Bitcoin is below your value !", "btc-logo.ico")
    elif btc > max_notify:
        toaster.show_toast("Limit notification", "Bitcoin is above your value !", "btc-logo.ico")


while True:
    load_state()
    time.sleep((60 * 15) - (time.time() - start_time) % (60 * 15))
