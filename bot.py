import ssl
import json
import websocket

def on_open(ws):
    print("Abriu a conexão. Aguarde uma transação ser realizada")

    json_subscribe = """
    {
        "event": "bts:subscribe",
        "data":{
            "channel": "live_trades_btcusd"
    """
    ws.send(json_subscribe)

def on_close(ws):
    pass

def erro(ws, erro):
    print("Deu erro")
    print(erro)

def message(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_message=message,
                                on_error=erro)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
