from xml.dom.minidom import parseString
import datetime
import urllib2
import sqlite3
import os

basepath = os.path.dirname(os.path.realpath(__file__))
con =sqlite3.connect(basepath + '/weather.db')
cur =con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS yrno
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
        element_time = datetime.datetime.strptime( child.getAttribute('from'), "%Y-%m-%dT%H:%M:%S" )
        element_data['date'] = element_time.strftime('%Y%m%d')
        element_data['unixtime'] = element_time.strftime('%s')
        element_data['period'] = child.getAttribute('period')
        element_data['symbol'] = child.getElementsByTagName('symbol')[0].getAttribute('number')
        element_data['temperature']  = child.getElementsByTagName('temperature')[0].getAttribute('value')
        element_data['wind_speed_mps'] = child.getElementsByTagName('windSpeed')[0].getAttribute('mps')
        element_data['wind_speed_name'] = child.getElementsByTagName('windSpeed')[0].getAttribute('name')
        element_data['wind_direction_deg'] = child.getElementsByTagName('windDirection')[0].getAttribute('deg')
        element_data['wind_direction_code'] = child.getElementsByTagName('windDirection')[0].getAttribute('code')

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

        con.execute(
                query,
                (element_data['date'],
                element_data['unixtime'],
                element_data['period'],
                element_data['symbol'],
                element_data['temperature'],
                element_data['wind_speed_mps'],
                element_data['wind_speed_name'],
                element_data['wind_direction_deg'],
                element_data['wind_direction_code'])
            )
    except AttributeError, e:
        #print e.__class__.__name__, e
        pass

con.commit()