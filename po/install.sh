#!/bin/bash
# This script is intended to be called from Makefile, it compiles and installs locales

DESTDIR=$1

# Compile
for locale in po/`cat po/LINGUAS`; do
	msgfmt $locale.po -o $locale.mo
done
# Install
for locale in `cat po/LINGUAS`; do
	install -d -m 755 $DESTDIR/usr/share/locale/$locale/LC_MESSAGES/
	mv po/$locale.mo $DESTDIR/usr/share/locale/$locale/LC_MESSAGES/samsung-tools.mo
done
