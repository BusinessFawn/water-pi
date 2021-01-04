#!/usr/bin/python

from flask import request
from flask_api import FlaskAPI
from gpiozero import LED

LEDS = {
    'red': {'led': LED(17), 'state': 'on'},
    'green': {'led': LED(27), 'state': 'on'},
    'blue': {'led': LED(4), 'state': 'on'}
}

for k,v in LEDS.items():
    print(f'off: {k}')
    v['led'].on()
    v['state'] = 'off'

app = FlaskAPI(__name__)


@app.route('/led', methods=['GET', 'DELETE'])
def api_root():
    if request.method == 'DELETE':
        for k, v in LEDS.items():
            LEDS[k]['led'].on()
            LEDS[k]['state'] = 'off'
    return {'status': 'OK', 'leds': {{k: v['state']} for k, v in LEDS.items()}}


@app.route('/led/<color>', methods=['POST', 'DELETE'])
def api_leds_control(color):
    if request.method == 'POST':
        if color in LEDS:
            LEDS[color]['led'].off()
            LEDS[color]['state'] = 'on'
            return {'status': 'OK', 'color': color}
        else:
            return {'status': 'ERROR', 'color': color}
    if request.method == 'DELETE':
        if color in LEDS:
            LEDS[color]['led'].on()
            LEDS[color]['state'] = 'off'
            return {'status': 'OK', 'color': color}
        else:
            return {'status': 'ERROR', 'color': color}


if __name__ == '__main__':
    app.run()
