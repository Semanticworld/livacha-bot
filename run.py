import requests
from bs4 import BeautifulSoup
import base64
import random
import json
import time
import websocket
from websocket import create_connection, WebSocket
import ssl

payload = {
    'login': '',
    'password': '',
    'remember': '1' }

pong = {
    'mess': 'pong'}

def auth():
    """TODO is to explain what things below doo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'application/json'
        }

#    headers['Sec-WebSocket-Key'] = str(base64.b64encode(bytes([random.randint(0, 255) for _ in range(16)])), 'ascii')
#    headers['Sec-WebSocket-Version'] = '13'
#    headers['Upgrade'] = 'websocket'

    session = requests.Session()
    r = session.get("https://livacha.com/login", headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    payload['_token'] =  soup.find("input", {"name":"_token"})["value"]

    print (payload)

    r = session.post("https://livacha.com/login", data=payload, headers=headers)
    r = session.get("https://livacha.com", headers=headers)

    f = open('result.html','w+')
    f.write(r.text)
    f.close()

    cookies = session.cookies.get_dict()
    headers['Cookie'] = "; ".join(["%s=%s" %(i, j) for i, j in cookies.items()])

    return headers


def on_message(ws, message):
    global timeout_timer
    global timeout_interval
    sending1 = {
        "mess": "chat",
        "data": {
            "text": "Извиние, но болтяра немного...."
        }
    }
    sending2 = {
        "mess": "chat",
        "data": {
            "text": "Извините, мы немножко пьяны..."
        }
    }
    sending3 = {
        "mess": "chat",
        "data": {
            "text": "Извините, я немножко пьян..."
        }
    }
    pong = {
        "mess": "pong",
        "data": {
            "from": "money",
            "imAlive": "1231231"
        }
    }
    print('### message ###')

    print('<< ' + message)

    message_object = json.loads(message)
    message_type   = message_object['mess']
    if( message_type == 'money' ):
#        print("### ping P#@#!@#")
        ws.send(json.dumps(pong))

    message_text = message_object['response']['text']
    if( 'пьян' in message_text):
        ws.send(json.dumps(sending1))


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
#    init = {
#        'type': 'connection_init'
#    }
#    init_conn = json.dumps(init)
#    print('>> '+ init_conn)
    init = {
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
            "room": "multik777"
        }
    }
    init_conn = json.dumps(init)
    print('>> '+ init_conn)
    ws.send(init_conn)

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

