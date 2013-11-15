#!/bin/bash
# This script is intended to be called from Makefile, it sets the work directory where needed

WORKDIR=$1

FILES=("backends/globals.py" "samsung-tools-preferences.py" "samsung-tools.py")

for file in ${FILES[*]}; do
	sed -i "s|WORK_DIRECTORY = .*|WORK_DIRECTORY = \"$WORKDIR\"|" $file
done
