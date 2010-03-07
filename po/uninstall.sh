#!/bin/bash
# This script is intended to be called from Makefile, it uninstalls locales

DESTDIR=$1

for locale in `cat po/LINGUAS`; do
	rm -rf $DESTDIR/usr/share/locale/$locale/LC_MESSAGES/samsung-tools.mo
done
