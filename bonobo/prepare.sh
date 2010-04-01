#!/bin/bash
# This script is intended to be called from Makefile, it prepares .server files

FILE="$1"
NEWFILE=`echo $FILE | sed 's:.in::'`

cat $FILE | sed 's:_value:value:' > $NEWFILE