from xml.dom.minidom import parse, parseString
import datetime
import sys
import sqlite3
con =sqlite3.connect('./weather.db')
cur =con.cursor()

replacetext = {
    'templo': 'lo',
    'temphi': 'hi',

    'temp00': '-',
    'temp01': '-',
    'temp02': '-',
    'temp03': '-',

    'temp10': '-',
    'temp11': '-',
    'temp12': '-',
    'temp13': '-',

    'temp20': '-',
    'temp21': '-',
    'temp22': '-',
    'temp23': '-',

    'day0': 'Today',
    'day1': 'Tomorrow',
    'day2': 'Next day',

    'icon00': 'yrno0',
    'icon01': 'yrno0',
    'icon02': 'yrno0',
    'icon03': 'yrno0',

    'icon10': 'yrno0',
    'icon11': 'yrno0',
    'icon12': 'yrno0',
    'icon13': 'yrno0',

    'icon20': 'yrno0',
    'icon21': 'yrno0',
    'icon22': 'yrno0',
    'icon23': 'yrno0',
}

# replace name of the days
replacetext['day0'] = datetime.datetime.now().strftime("%A")
replacetext['day2'] = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%A")

now = datetime.datetime.today()
today = datetime.datetime(now.year, now.month, now.day)
cur.execute("SELECT wdate, period, symbol, temperature, wind_speed_mps, wind_speed_name, wind_direction_deg, wind_direction_code FROM yrno WHERE tstamp in (SELECT max(tstamp) FROM yrno WHERE unixtime >= ? GROUP BY wdate,period) ORDER BY unixtime;", (int(today.strftime('%s')),))

templo = 100
temphi = 0

rows = cur.fetchall()
for row in rows:
    wdate = datetime.datetime.strptime(row[0],'%Y%m%d')
    delta_days = (wdate - today).days
    data_id = str(delta_days) + str(row[1])
    if delta_days > 2:
        break

    if delta_days == 0:
        if templo > int(row[3]):
            templo = int(row[3])
        if temphi < int(row[3]):
            temphi = int(row[3])

    replacetext['temp'+data_id] = str(row[3])
    replacetext['icon'+data_id] = "yrno" + str(row[2])

    print data_id

replacetext['templo'] = templo
replacetext['temphi'] = temphi

template_doc = parse("./icons/new_template.svg")




for el in template_doc.getElementsByTagName('text'):
    try:
        if el.attributes["id"].value in replacetext:
            #print el.attributes["id"].value + "->" + replacetext[el.attributes["id"].value]
            el.firstChild.nodeValue = str(replacetext[el.attributes["id"].value])

    except KeyError:
        pass

for el in template_doc.getElementsByTagName('use'):
    try:
        if el.attributes["id"].value in replacetext:
            el.attributes["xlink:href"].value = '#'+replacetext[el.attributes["id"].value]
            print el.attributes["xlink:href"].value

    except KeyError:
        pass


fh = open("output.svg","wb")
template_doc.writexml(fh)
fh.close()