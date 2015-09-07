#! /bin/sh

S=0;

while true; do
        N=$(hexdump -n 13 /dev/input/event0 | ./parse_event0.sh "$S");
        echo "N=$N";
        S=$N
done