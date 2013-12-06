#!/usr/bin/env python2
import gevent.monkey
gevent.monkey.patch_all()

import flask
from flask import Flask
from flask_sockets import Sockets
import gevent
import gevent.queue
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__, static_url_path='')

sockets = Sockets(app)
seekers = gevent.queue.Queue()


def relay(from_, to):
    """route messges from_ -> to"""
    try:
        while True:
            to.send(from_.receive())
    except:
        # Notify to about disconnection - unless to disconnected
        try: to.send("Peer disconnected.")
        except: pass


def session(ws1, ws2):
    for ws in [ws1, ws2]:
        ws.send("/Found a person. Say hello")
    gevent.joinall([
        gevent.spawn(relay, ws1, ws2),
        gevent.spawn(relay, ws2, ws1)
    ])


def matcher(seekers):
    while True:
        gevent.spawn(session, seekers.get(), seekers.get())

gevent.spawn(matcher, seekers)

@sockets.route('/ws')
def websocket(ws):
    seekers.put(ws)
    ws.send("/Welcome. Seeking a partner")
    while True:  # hack to keep the greenlet alive
        gevent.sleep(0.5)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler) \
          .serve_forever()
