import requests

def send_ping():
    url = 'http://127.0.0.1:3251'
    routing = '/ping'
    x = requests.get(url + routing)
    return x