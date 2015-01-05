#! /bin/sh

# create a svg
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
/usr/bin/python "${DIR}/create_svg.py"

# convert to png
/usr/bin/convert "${DIR}/output.svg" "${DIR}/output.png"

# convert to raw
/usr/local/bin/ffmpeg -i "${DIR}/output.png" -vf transpose=2 -f rawvideo -pix_fmt rgb565 -s 800x600 -y "${DIR}/output.raw" < /dev/null

# compress
# gzip "${DIR}/output.raw"

# move to webspace
mv "${DIR}/output.raw" /mnt/www/tmp/