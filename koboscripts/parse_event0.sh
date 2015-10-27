#! /bin/sh

S=$1
read i
data=$(echo $i|tail -c 8)

# top button down: 0074 0001
# top button up: 0074 0000
if echo $data | grep "74 0001" >/dev/null 2>&1; then
	echo -n 1
	reboot
fi

# front button down: 66 0001
# front button up: 66 0000
if echo $data | grep "66 0000" >/dev/null 2>&1; then
        if [ $S -eq 0 ]; then
                /mnt/onboard/restart_nickle.sh
                echo -n 1
        else
                echo -n 0
        fi
else
        echo $S
fi
#echo $data | grep "66 0000" >/dev/null 2>&1 && /mnt/onboard/restart_nickle.sh