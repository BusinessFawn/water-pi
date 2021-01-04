# Why?

Users might want a way to use a Raspberry Pi as a controller for various types of hardware. The easiest/most convenient
way I know to do that is through a RESTful API in Python.

For this specific project I wanted a way to make sure that components didn't stay on past what was reasonable. To
achieve this there is a thread that controls the hardware and then checks a queue looking for a message to stop the
current operation.

# Usage

Running this locally on the Pi:

1. copy repo
    * `git clone https://github.com/BusinessFawn/water-pi.git`
1. go to correct dir
    * `cd water-pi/`
1. start server
    * `bash run_led_pi_api.sh`