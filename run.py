from bs4 import BeautifulSoup
import base64
import json
import os
import random
import requests
import ssl
import time
import websocket
from websocket import create_connection, WebSocket


login = os.environ.get('LIVACHA_USER')
password = os.environ.get('LIVACHA_PASS')

payload = {
    'login': login,
    'password': password,
    'remember': '1' }

multik = {
"mess": "chat",
"data": {
    "text": "Извините, но Рома немножко пьян...."}}

hello = {
"mess": "chat",
"data": {
    "text": "Здарова Земеля, как сам?"}}

pong = {
"mess": "pong",
"data": {
    "from": "money",
    "imAlive": "1231231"}}

headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'application/json'}

join = {
        "mess": "join",
        "data": {
            "extended": {
                "birth": "2005-02-01",
                "city": "20317",
                "height": "null",
                "relat": "null",
                "sex": "m",
                "text": "null",
                "weight": "null"
            },
            "room": 'uniq_roomid'
        }
}

leave = {
        "mess": "leave",
        "data": {
            "extended": {
                "birth": "2005-02-01",
                "city": "20317",
                "height": "null",
                "relat": "null",
                "sex": "m",
                "text": "null",
                "weight": "null"
            },
            "room": 'uniq_roomid'
        }
}


find_message = "Мультик"

def auth():
    """Auth section to get cookies"""

    session = requests.Session()
    r = session.get("https://livacha.com/login", headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    payload['_token'] =  soup.find("input", {"name":"_token"})["value"]

    print (payload)

    r = session.post("https://livacha.com/login", data=payload, headers=headers)
    r = session.get("https://livacha.com", headers=headers)

    cookies = session.cookies.get_dict()
    headers['Cookie'] = "; ".join(["%s=%s" %(i, j) for i, j in cookies.items()])

    return headers

def roomSwitcher(ws,message):
    print ('### Room Switcher###')
    ws.send(json.dumps(leave))
    init_conn = json.dumps(join)
    message_object = json.loads(message)
    if(message_object['response']['type'] == "publish"):
        roomid = message_object['response']['room']['alias']
        init_conn = json.dumps(join).replace("uniq_roomid",roomid)
        ws.send(init_conn)
        time.sleep(10)
        ws.send(json.dumps(hello))

def on_message(ws, message):
    global timeout_timer
    global timeout_interval

    print('### message ###')

    print('<< ' + message)

    message_object = json.loads(message)
    message_type   = message_object['mess']
    if( message_type == 'money' ):
        ws.send(json.dumps(pong))

    if( message_type == 'streamsUpdate' ):
        roomSwitcher(ws,message)

    if( message_type == 'message' ):
        message_text = message_object['response']['textRaw']
        if( find_message in message_text):
            ws.send(json.dumps(multik))

def on_error(ws, error):
    print('### error ###')
    print(error)

def on_ping(ws, error):
    print('### Ping recieved ###')
    print(error)

def on_close(ws):
    print('### closed ###')

def on_open(ws):
    print('### opened ###')
    init_conn = json.dumps(join)
    print('>> '+ init_conn)
#    ws.send(init_conn)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://livacha.com:8443',
                        header=auth(),
                        on_open = on_open,
                        on_message = on_message,
                        on_error = on_error,
                        on_close = on_close,
                        on_ping = on_ping)

    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

