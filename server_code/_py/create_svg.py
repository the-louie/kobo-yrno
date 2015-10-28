from xml.dom.minidom import parse
from datetime import datetime, timedelta
from sqlite3 import connect
from sys import maxint

DBCON = connect('./weather.db')
DBCUR = DBCON.cursor()

# some basic defaults, not needed.
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

    'gentime': 'unknown'
}

# update gentime
replacetext['gentime'] = datetime.now().strftime("%Y%m%d %H:%M")

# replace name of the days
replacetext['day0'] = datetime.now().strftime("%A")
replacetext['day2'] = (datetime.now() + timedelta(days=2)).strftime("%A")

# get unixtime for start of today
now = datetime.today()
today = datetime(now.year, now.month, now.day)

# get data from start of today and forward
DBCUR.execute("""SELECT
            wdate,
            period,
            symbol,
            temperature,
            wind_speed_mps,
            wind_speed_name,
            wind_direction_deg,
            wind_direction_code
        FROM
            yrno
        WHERE
            tstamp IN (
                SELECT
                    max(tstamp)
                FROM
                    yrno
                WHERE
                    unixtime >= ?
                GROUP BY
                    wdate,period
            )
        ORDER BY
            unixtime;""", (int(today.strftime('%s')),))

# preset templo and temphi to unreasonable values
templo = maxint
temphi = -maxint

# fetch data from the database
rows = DBCUR.fetchall()
for row in rows:
    wdate = datetime.strptime(row[0],'%Y%m%d') # date for forecast
    delta_days = (wdate - today).days
    data_id = str(delta_days) + str(row[1])    # use delta days to get day id
    if delta_days > 2: # only look two days ahead
        break

    if delta_days == 0: # get min/max for the current day
        if templo > int(row[3]):
            templo = int(row[3])
        if temphi < int(row[3]):
            temphi = int(row[3])

    # add text to replace in replacetext dict
    replacetext['temp'+data_id] = str(row[3])
    replacetext['icon'+data_id] = "yrno" + str(row[2])

# add templo and temphi to replacetext
replacetext['templo'] = templo
replacetext['temphi'] = temphi


# load svg template as xml
template_doc = parse("./icons/new_template.svg")

# find all text elements and change their content
# if the element has a matching id-tag in replacetext
for el in template_doc.getElementsByTagName('text'):
    try:
        if el.attributes["id"].value in replacetext:
            newval = str(replacetext[el.attributes["id"].value])
            el.firstChild.nodeValue = newval

    except KeyError:
        pass

# find all use-tags and replace their link if the
# id has a matching string in replacetext
for el in template_doc.getElementsByTagName('use'):
    try:
        if el.attributes["id"].value in replacetext:
            newval = '#'+replacetext[el.attributes["id"].value]
            el.attributes["xlink:href"].value = newval

    except KeyError:
        pass


# save the result as an svg
fh = open("./tmp/output.svg","wb")
template_doc.writexml(fh)
fh.close()