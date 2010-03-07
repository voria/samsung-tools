#!/bin/bash

echo "*** Extracting strings from *.glade files..."
intltool-extract --type=gettext/glade gui/glade/*.glade
mv gui/glade/*.glade.h .

echo
echo "*** Creating messages.pot..."
xgettext -k_ -kN_ -o po/messages.pot `cat po/FILES` *.glade.h

echo
echo "*** Removing unneeded files..."
rm *.glade.h

for locale in `cat po/LINGUAS`; do
	if [ -f po/$locale.po ]; then
		echo "*** Updating '`echo $locale.po | cut -d/ -f2`'..."
		msgmerge -U po/$locale.po po/messages.pot
	else
		echo "*** Creating new '`echo $locale.po | cut -d/ -f2`'..."
		cp po/messages.pot po/$locale.po
	fi
done

echo
echo "Done."