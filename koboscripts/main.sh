#! /bin/sh

# kill nickel and hindenburg so they stop
# interfering with us
echo "killing nickel and hindenburg"
killall nickel || killall -9 nickel
killall hindenburg || killall -9 hindenburg

# get the rest of the scripts
cat /mnt/onboard/images/scripts0.raw | /usr/local/Kobo/pickel showpic
echo "fetching the rest of the scripts"
SCRIPTLIST="button_wrapper.sh parse_event0.sh wifidn.sh wifiup.sh update.sh sleep.sh"
for S in $SCRIPTLIST; do
	echo " * $S"
	wget -O /mnt/onboard/scripts/$S -q http://31.31.164.43/labb/kobo/$S
done

# failsaife to use button to load nickel again
cat /mnt/onboard/images/button0.raw | /usr/local/Kobo/pickel showpic
echo "starting button failsafe"
cd /mnt/onboard/scripts/
nohup /mnt/onboard/scripts/button_wrapper.sh &

echo "entering update loop"
cat /mnt/onboard/images/update0.raw | /usr/local/Kobo/pickel showpic
while true; do
	/mnt/onboard/scripts/update.sh
	usleep 3600000000 # sleep for an hour
done
