from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from time import sleep

from gpiozero import LED

queue = Queue()
wait_time = .5
executor = ThreadPoolExecutor(max_workers=1)


class ThreadLed:
    """
    Allows a threaded instance to control the lights on a Raspberry Pi.
    Using this method allows the user to set timeouts so that if for some reason the Pi stops getting
    signals because of a code issue the operation will terminate after a certain amount of time.
    """

    def __init__(self):
        self.engaged = {'engaged': True}
        self.LEDS = {
            'red': {'led': LED(17), 'state': 'on'},
            'green': {'led': LED(27), 'state': 'on'},
            'blue': {'led': LED(4), 'state': 'on'}
        }
        for k, v in self.LEDS.items():
            # print(f'off: {k}')
            v['led'].on()
            v['state'] = 'off'
        self.engaged['engaged'] = False

    def turn_on_lights(self, colors: dict) -> None:
        if self.engaged['engaged']:
            # print('putting message on queue')
            queue.put('some_message')

        for i in range(5):
            if not self.engaged['engaged']:
                executor.submit(manipulate_and_wait, self.engaged, self.LEDS, colors)
                # print('lights are on')
                return
            # print('lights on retry')
            sleep(wait_time)

        raise Exception("Error trying to start the threads")

    def turn_off_lights(self) -> None:

        if self.engaged['engaged']:
            # print('putting message on queue')
            queue.put('some_message')

        for i in range(5):
            if not self.engaged['engaged']:
                # print('lights are off')
                return
            # print('lights off retry')
            sleep(wait_time)

        raise Exception("Error trying to start the threads")


def manipulate_and_wait(engaged: dict, leds: dict, colors: dict) -> None:
    engaged['engaged'] = True
    max_checks = 180
    for light in colors:
        if colors[light]:
            leds[light]['led'].off()
            leds[light]['state'] = 'on'
    # print('thread lights on')
    while max_checks:
        try:
            queue.get(timeout=wait_time)
            break
        except Exception as e:
            # print(f'ex: {e}')
            pass
        max_checks -= 1

    for k, v in leds.items():
        # print(f'off: {k}')
        v['led'].on()
        v['state'] = 'off'
    # print('thread lights off')
    engaged['engaged'] = False


if __name__ == '__main__':
    from utils.fake_leds import FakeLEDS as LED

    thread_led = ThreadLed()

    thread_led.turn_on_lights({'red': True})
    print('lights on: red')
    sleep(1)
    thread_led.turn_on_lights({'blue': True, 'green': True, 'red': False})
    print('lights on: blue, green')
    sleep(1.5)
    thread_led.turn_off_lights()
    print('lights off')
    print(thread_led.engaged)
