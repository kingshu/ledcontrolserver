import ephem

def isDarkOutside():
    sun = ephem.Sun()
    seattle = ephem.city('Seattle')
    sun.compute(seattle)
    twilight = -12 * ephem.degree
    return sun.alt < twilight
