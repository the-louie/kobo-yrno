from xml.dom.minidom import parseString
import datetime
import urllib2
import sqlite3
import os
import sys

BASEPATH = os.path.dirname(os.path.realpath(__file__))
DBCON = sqlite3.connect(BASEPATH + '/db/weather.db')
DBCUR = DBCON.cursor()

DBCUR.execute("""CREATE TABLE IF NOT EXISTS yrno
        (tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        wdate TEXT,
        unixtime INT,
        period INT,
        symbol INT,
        temperature REAL,
        wind_speed_mps REAL,
        wind_speed_name TEXT,
        wind_direction_deg REAL,
        wind_direction_code TEXT)
    """)


def elattr(root, elname, attrname):
    el = root.getElementsByTagName(elname)[0]
    attr = el.getAttribute(attrname)
    return attr


# get yr.no data
response = urllib2.urlopen('http://www.yr.no/place/Sweden/J%C3%B6nk%C3%B6ping/J%C3%B6nk%C3%B6ping/forecast.xml')
html = response.read()
if html is None:
    print "no response from server"
    sys.exit(1)


data_doc = parseString(html)
tabular = data_doc.getElementsByTagName('tabular')[0]

for child in tabular.childNodes:
    element_data = {}
    try:
        element_time = datetime.datetime.strptime(
                child.getAttribute('from'),
                "%Y-%m-%dT%H:%M:%S")
        element_data['date'] = element_time.strftime('%Y%m%d')
        element_data['unixtime'] = element_time.strftime('%s')
        element_data['period'] = child.getAttribute('period')
        element_data['symbol'] = elattr(child, 'symbol', 'number')
        element_data['temperature']  = elattr(child, 'temperature', 'value')
        element_data['wind_speed_mps'] = elattr(child, 'windSpeed', 'mps')
        element_data['wind_speed_name'] = elattr(child, 'windSpeed', 'name')
        element_data['wind_dir_deg'] = elattr(child, 'windDirection', 'deg')
        element_data['wind_dir_code'] = elattr(child, 'windDirection', 'code')

        #print element_data
        query = """INSERT INTO yrno (
                wdate,
                unixtime,
                period,
                symbol,
                temperature,
                wind_speed_mps,
                wind_speed_name,
                wind_direction_deg,
                wind_direction_code
            ) VALUES (
                ?,?,?,?,?,?,?,?,?
            )"""

        DBCUR.execute(
                query,
                (element_data['date'],
                element_data['unixtime'],
                element_data['period'],
                element_data['symbol'],
                element_data['temperature'],
                element_data['wind_speed_mps'],
                element_data['wind_speed_name'],
                element_data['wind_dir_deg'],
                element_data['wind_dir_code'])
            )
    except AttributeError, e:
        #print e.__class__.__name__, e
        pass

DBCON.commit()