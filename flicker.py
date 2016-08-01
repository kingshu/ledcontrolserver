import pigpio
import time

PIN_RED = 24
PIN_GRN = 25
PIN_BLU = 14

def setToColor1(pi):
    pi.set_PWM_dutycycle(PIN_RED, 227)
    pi.set_PWM_dutycycle(PIN_GRN, 58)
    pi.set_PWM_dutycycle(PIN_BLU, 32)

def setToColor2(pi):
    pi.set_PWM_dutycycle(PIN_RED, 227)
    pi.set_PWM_dutycycle(PIN_GRN, 198)
    pi.set_PWM_dutycycle(PIN_BLU, 32)

def setToColor3(pi):
    pi.set_PWM_dutycycle(PIN_RED, 255)
    pi.set_PWM_dutycycle(PIN_GRN, 173)
    pi.set_PWM_dutycycle(PIN_BLU, 148)


def flicker(pi):
    i=20
    while (i>0):
        setToColor1(pi)
        time.sleep(0.05)
        setToColor2(pi)
        time.sleep(0.05)
        setToColor3(pi)
        time.sleep(0.05)
        i-=1
        if i%5 == 0:
            time.sleep(1)

def pulse(pi, currState):
    targetColor = {}
    targetColor['red'] = 255 - int(currState['red'])
    targetColor['green'] = 255 - int(currState['green'])
    targetColor['blue'] = 255 - int(currState['blue'])
    i = {}
    i['red'] = targetColor['red']
    i['green'] = targetColor['green']
    i['blue'] = targetColor['blue']

    count = 1
    while count < 20:
        pi.set_PWM_dutycycle(PIN_RED, i['red'])
        pi.set_PWM_dutycycle(PIN_GRN, i['green'])
        pi.set_PWM_dutycycle(PIN_BLU, i['blue'])
        i['red'] += (int(currState['red']) - targetColor['red'])/20
        i['green'] += (int(currState['green']) - targetColor['green'])/20
        i['blue'] += (int(currState['blue']) - targetColor['blue'])/20
        time.sleep(0.07)
        count += 1