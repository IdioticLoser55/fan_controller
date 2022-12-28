import gpiod
import time
import sys
import os

ON_TMP = 60
OFF_TMP = 50

chip = gpiod.chip(0)
pwm_pin = chip.get_line(12)

config = gpiod.line_request()
config.consumer = "pwm fan"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

pwm_pin.request(config)


def get_cpu_temperature():
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    temp1 = float((res.replace("temp=","").replace("'C\n","")))
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    temp2 = float(res.replace("'C\n", "")) / 1000

    print(str(temp1) + "  " + str(temp2))
    if(temp1 > temp2):
        temp = temp1
    else:
        temp = temp2

    return temp

try:
    while True:
        temp = get_cpu_temperature()
        if(temp > ON_TMP):
            pwm_pin.set_value(1)
        if(temp < OFF_TMP):
            pwm_pin.set_value(0)
            time.sleep(500)
            continue
        time.sleep(20)

except KeyboardInterrupt:
    pass
