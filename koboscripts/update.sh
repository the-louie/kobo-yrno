#!/bin/sh
# sh /mnt/onboard/wifiup.sh
battery=`cat /sys/devices/platform/pmic_battery.1/power_supply/mc13892_bat/capacity`
# url="http://qnap/modules/wetter/kobo.php?bat="
# url_all=$url$battery
# wget -q -s $url_all
# sleep 5
# rm /mnt/onboard/kobo.raw.gz
wget -O - "http://31.31.164.43/tmp/output.raw?bat=${battery}" | /usr/local/Kobo/pickel showpic
#wget -q -O - http://31.31.164.43/modules/wetter/kobo.raw.gz -P /mnt/onboard/
#zcat /mnt/onboard/kobo.raw.gz | /usr/local/Kobo/pickel showpic
#sh /mnt/onboard/wifidn.sh
#sh /mnt/onboard/sleep.sh
