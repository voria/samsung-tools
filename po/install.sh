#!/bin/bash
# This script is intended to be called from Makefile, it compiles and installs locales

PREFIX=$1

# Compile
for locale in `cat po/LINGUAS`; do
	msgfmt po/$locale.po -o po/$locale.mo
done
# Install
for locale in `cat po/LINGUAS`; do
	install -d -m 755 $PREFIX/share/locale/$locale/LC_MESSAGES/
	install -pm 644 po/$locale.mo $PREFIX/share/locale/$locale/LC_MESSAGES/samsung-tools.mo
	rm -f po/$locale.mo
done
