#!/usr/bin/python

from flask import request
from flask_api import FlaskAPI
from utils.led_util import ThreadLed

app = FlaskAPI(__name__)

thread_led = ThreadLed()


@app.route('/led', methods=['GET', 'DELETE'])
def api_root():
    if request.method == 'DELETE':
        thread_led.turn_off_lights()
    led_colors = {}
    for k, v in thread_led.LEDS.items():
        led_colors[k] = v['state']
    return {'status': 'OK', 'leds': led_colors}


@app.route('/led/<color>', methods=['POST', 'DELETE'])
def api_leds_control(color):
    if request.method == 'POST':
        if color in thread_led.LEDS:
            colors = {col: True for col, v in thread_led.LEDS.items() if v['state'] == 'on'}
            if color in colors:
                return {'status': 'ERROR', 'color': color, 'reason': 'color already on'}
            colors[color] = True
            thread_led.turn_on_lights(colors)
            return {'status': 'OK', color: 'on'}
        else:
            return {'status': 'ERROR', 'color': color}
    if request.method == 'DELETE':
        if color in thread_led.LEDS:
            colors = {col: True for col, v in thread_led.LEDS.items() if v['state'] == 'on' and col != color}
            if not colors:
                thread_led.turn_off_lights()
            else:
                thread_led.turn_on_lights(colors)
            return {'status': 'OK', color: 'off'}
        else:
            return {'status': 'ERROR', 'color': color}


if __name__ == '__main__':
    app.run()
