import ssl
import json
import websocket
import bitstamp.client #essa é uma biblioteca que achei no github
import credenciais


def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME, #no arquivo credenciais muda pro seu usuário
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)


def comprar(quantidade): #apenas um exemplo de compra. Compra quando o valor do bitcoin está no valor de mercado
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)


def vender(quantidade): #apenas um exemplo de venda. Vende quando o valor do bitcoin está no valor de mercado
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)

def on_open(ws): #As funções on_algo é o código do prórpio bitstamp que eles disónibilizaram
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

def on_erro(ws, erro):
    print("Deu erro")
    print(erro)

def on_message(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)
    
    #uma pequena lógica pra vompra e venda
    if price > 10000:
        vender()
    elif price < 8100:
        comprar()
    else:
        print("Aguardar")

#A main também é do bitstamp
if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_erro)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
