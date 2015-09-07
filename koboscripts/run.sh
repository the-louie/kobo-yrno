#! /bin/sh

echo "run.sh started "$(date | tr -d '\n')
echo "sleeping for 30s"
sleep 30

# clear old scripts
echo "clearing old scripts"
rm -rf /mnt/onboard/scripts
mkdir -p /mnt/onboard/scripts

# enable networking
echo "enable networking"
/bin/sh /mnt/onboard/wifiup.sh

echo "wait a while..."
usleep 500000 # sleep for 5 seconds

# try to download script to run
echo "fetching main.sh"
while ! wget -T 10 -O /mnt/onboard/scripts/main.sh -q http://31.31.164.43/labb/kobo/main.sh; do
	echo " * fail"
	usleep 1000000 # sleep for 10 seconds
done

# run script
echo "running main.sh"
/bin/sh /mnt/onboard/scripts/main.sh
