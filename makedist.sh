#!/bin/sh
VERSION=`/usr/bin/grep "version = '" soa/code.py | /usr/bin/cut -f2 -d\' | /usr/bin/sed 's/\./_/'`
OUTPUT_FILE="soa_${VERSION}.zip"
/usr/bin/zip -r ${OUTPUT_FILE} soa
echo
echo "File $OUTPUT_FILE written"
exit 0
