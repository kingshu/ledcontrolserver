import pigpio
import json
import urllib

def setColor(rPath):

    badResp = {'ERROR': 'BAD COLOR DESCRIPTOR'}

    if validRGB(rPath):
        rPath = adjustForElliesFavoriteColor(rPath)
        return {'red':rPath[2], 'green':rPath[3], 'blue':rPath[4], 'power':'on'}
    else:
        with open('/home/pi/ledcontrolserver/colorsToRgb.json') as json_data:
            colors = json.load(json_data)
            try:
                colorName = str(urllib.unquote(str(rPath[2])).decode('utf8')).lower()
            except:
                return badResp
            if colorName in colors:
                return {'red':(colors[colorName])[0], 'green':(colors[colorName])[1], 'blue':(colors[colorName])[2], 'power':'on'}
    return badResp

def adjustForElliesFavoriteColor(rgb):
    if (int(rgb[2])==126 and int(rgb[3])==255 and int(rgb[4])==210):
        rgb[2] = 0
        rgb[3] = 255
        rgb[4] = 74
    return rgb

def validRGB(rgbList):
    if len(rgbList) != 5:
        return False
    for i in range(2, len(rgbList)-1):
        if int(rgbList[i])<0 or int(rgbList[i])>255:
            return False;
    return True;
