#! /bin/sh

# start wifi
insmod /drivers/ntx508/wifi/sdio_wifi_pwr.ko
insmod /drivers/ntx508/wifi/dhd.ko

exit

# standard

# stop these in init.d/rcS instead
# sleep 10
# killall nickel
# killall hindenburg
# sleep 10


crond &
sleep 2

# do this change the led behaviour?
echo "ch 4" > /sys/devices/platform/pmic_light.1/lit # channel 4 is the led
echo "cur 0" > /sys/devices/platform/pmic_light.1/lit # turn off the led (current -> 0)
echo "dc 0" > /sys/devices/platform/pmic_light.1/lit # turn off the led (PWM cycle -> 0)

cat /mnt/onboard/testimage.raw | /usr/local/Kobo/pickel showpic


sleep 3
#/bin/sh /mnt/onboard/update.sh
