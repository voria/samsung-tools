#!/bin/bash
# This script is intended to be called from Makefile, it prepares .desktop files

FILE="$1"
NEWFILE=`echo $FILE | sed 's:.in::'`

cat $FILE | sed 's:_Name:Name:' | sed 's:_Comment:Comment:' > $NEWFILE