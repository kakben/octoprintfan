import RPi.GPIO as GPIO
import time
from subprocess import PIPE, Popen

def get_cpu_temperature():
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

FAN_CTRL_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(FAN_CTRL_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    last_switch_low = True
    while True:
        temp = get_cpu_temperature()
        print(temp)
        if temp > 39.6:
            GPIO.output(FAN_CTRL_PIN, GPIO.HIGH)
            if last_switch_low == True:
                print("Turning fan on, too hot! ({:.1f})".format(temp))
                last_switch_low = False
        elif temp < 38.5:
            GPIO.output(FAN_CTRL_PIN, GPIO.LOW)
            if last_switch_low == False:
                print("Turning fan off, cool enough. ({:.1f})".format(temp))
                last_switch_low = True
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print ""
