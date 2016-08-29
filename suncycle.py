import requests
import json
import time

def isDarkOutside():
    sunset = getSunsetEpoch()
    sunrise = getSunriseEpoch()
    if not sunset or not sunrise:
        return True # err on side of darkness
    now = getCurrentEpoch()
    print "Now:     "+str(now)
    print "Sunset:  "+str(sunset)
    print "Sunrise: "+str(sunrise)
    return now > sunset and now < sunrise

def getSunsetEpoch():
    url_today = "http://api.sunrise-sunset.org/json?lat=47.608419&lng=-122.327904&date=today"
    r = requests.get(url_today)
    if int(r.status_code) == 200:
        resp = json.loads(r.content)
        return convertToEpoch(resp["results"]["sunset"], 0)
    else:
        return False

def getSunriseEpoch():
    url_tomorrow = "http://api.sunrise-sunset.org/json?lat=47.608419&lng=-122.327904&date=tomorrow"
    r = requests.get(url_tomorrow)
    if int(r.status_code) == 200:
        resp = json.loads(r.content)
        return convertToEpoch(resp["results"]["sunrise"], 1)
    else:
        return False

def getCurrentEpoch():
    return time.time()

# relative_day = 0 for today, 2 for day after tomorrow, -9 for 9 days ago
def convertToEpoch(timeToConvert, relative_day=0):
    pattern = '%Y-%m-%d %H:%M:%S %p'
    absolute_date = time.strftime("%Y-%m-%d", time.localtime(time.time()+24*3600*int(relative_day)))
    full_datetime = absolute_date +" "+ timeToConvert
    return int(time.mktime(time.strptime(full_datetime, pattern)))
