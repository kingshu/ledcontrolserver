import requests
import json
import time

def isDarkOutside():
    sunset = getSunsetEpoch()
    sunrise = getSunriseEpoch()
    if not sunset or not sunrise:
        return True # err on side of darkness
    now = getCurrentEpoch()
    return now > sunset and now < sunrise

def getSunsetEpoch():
    url_today = "http://api.sunrise-sunset.org/json?lat=47.608419&lng=-122.327904&date=today"
    r = requests.get(url_today)
    if int(r.status_code) == 200:
        resp = json.loads(r.content)
        return convertToEpoch(resp["results"]["sunset"])
    else:
        return False

def getSunriseEpoch():
    url_tomorrow = "http://api.sunrise-sunset.org/json?lat=47.608419&lng=-122.327904&date=tomorrow"
    r = requests.get(url_tomorrow)
    if int(r.status_code) == 200:
        resp = json.loads(r.content)
        return convertToEpoch(resp["results"]["sunrise"])
    else:
        return False

def getCurrentEpoch():
    return time.time()

def convertToEpoch(timeToConvert):
    pattern = '%Y-%m-%d %H:%M:%S %p'
    tomorrow_date = time.strftime("%Y-%m-%d", time.localtime(time.time()+24*3600))
    full_datetime = tomorrow_date +" "+ timeToConvert
    return int(time.mktime(time.strptime(full_datetime, pattern)))