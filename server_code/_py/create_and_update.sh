#! /bin/sh

# chpwd to script directory
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# create a svg
echo "create_svg.py"
/usr/bin/python "${DIR}/create_svg.py"

# convert to png
echo "convert"
/usr/bin/convert "${DIR}/tmp/output.svg" "${DIR}/tmp/output.png"

# convert to raw
echo "ffmpeg"
/usr/local/bin/ffmpeg -i "${DIR}/tmp/output.png" -vf transpose=2 -f rawvideo -pix_fmt rgb565 -s 800x600 -y "${DIR}/tmp/output.raw" < /dev/null

# compress
# echo "gzip"
# gzip "${DIR}/tmp/output.raw"

# move to webspace
echo "mv"
mv "${DIR}/tmp/output.raw" /mnt/www/tmp/