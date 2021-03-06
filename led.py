import pigpio
import time
import json
import requests
import suncycle
import flicker
import color
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PIN_RED = 24
PIN_GRN = 25
PIN_BLU = 18

PORT_NUMBER = 8080
pi = pigpio.pi()

CURR_LED_STATE = {'red':0, 'green':0, 'blue':0}
POWER = False;

class myHandler(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(60)

    def do_GET(self):
        
        global pi
        global CURR_LED_STATE
        global POWER

        self.send_response(200)
        self.send_header('Content-type','application/javascript')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        rPath = self.path.split('/')
        try:
            if rPath[1] == "getstate":
                if POWER:
                    resp = CURR_LED_STATE
                else:
                    resp = {'red':0, 'green':0, 'blue':0, 'power':'off'}
            elif rPath[1] == "turnoff":
                turnoff()
                resp = {'SUCCESS':'TURNED OFF'}
            elif rPath[1] == "turnon":
                turnon()
                resp = CURR_LED_STATE;
                resp['SUCCESS'] = 'TURNED ON'
            elif rPath[1] == "setstate":
                resp = color.setColor(rPath)
                if 'ERROR' not in resp:
                    CURR_LED_STATE = resp
                    pi.set_PWM_dutycycle(PIN_RED, CURR_LED_STATE['red'])
                    pi.set_PWM_dutycycle(PIN_GRN, CURR_LED_STATE['green'])
                    pi.set_PWM_dutycycle(PIN_BLU, CURR_LED_STATE['blue'])
            elif rPath[1] == "flicker":
                flicker.flicker(pi)
                resp = {'SUCCESS':'FLICKERED'}
		if POWER:
                    turnon()
                else:
                    turnoff()
            elif rPath[1] == "pulse":
                flicker.pulse(pi, CURR_LED_STATE)
                resp = {'SUCCESS':'PULSED'}
                if POWER:               
                    turnon()
                else:
                    turnoff()
            elif rPath[1] == "turnonifdark":
                if suncycle.isDarkOutside():
                    turnon()
                    resp = CURR_LED_STATE;
                    resp['SUCCESS'] = 'TURNED ON'
                else:
                    resp = {'SUCCESS':'NOT DARK YET'}
            else:
                resp = {'ERROR': 'UNKNOWN ENDPOINT'}
        except IndexError:
            resp = {'ERROR': 'INVALID REQUEST'}
            
        self.wfile.write(json.dumps(resp))
        return

def turnoff():

    global pi
    global POWER

    pi.set_PWM_dutycycle(PIN_RED, 0)
    pi.set_PWM_dutycycle(PIN_GRN, 0)
    pi.set_PWM_dutycycle(PIN_BLU, 0)
    POWER = False;

def turnon():

    global pi
    global CURR_LED_STATE
    global POWER

    pi.set_PWM_dutycycle(PIN_RED, CURR_LED_STATE['red'])
    pi.set_PWM_dutycycle(PIN_GRN, CURR_LED_STATE['green'])
    pi.set_PWM_dutycycle(PIN_BLU, CURR_LED_STATE['blue'])
    POWER = True;

try:
    turnoff()
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
    turnoff()
    pi.stop()
