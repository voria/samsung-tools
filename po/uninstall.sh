#!/bin/bash
# This script is intended to be called from Makefile, it uninstalls locales

PREFIX=$1

for locale in `cat po/LINGUAS`; do
	rm -f $PREFIX/share/locale/$locale/LC_MESSAGES/samsung-tools.mo
done
