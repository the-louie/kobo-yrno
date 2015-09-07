#! /bin/sh

S=$1
read i
data=$(echo $i|tail -c 8)
# button up
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