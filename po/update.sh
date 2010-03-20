#!/bin/bash
# This script creates a new template 'samsung-tools.pot', and updates all translations against it

echo "*** Extracting strings from *.glade files..."
for file in gui/glade/*.glade; do
	intltool-extract --type=gettext/glade "$file"
done
mv gui/glade/*.glade.h po/

echo "*** Extracting strings from *.desktop files..." # A bit hacking, but it works
for file in desktop/*.desktop.in; do
	intltool-extract --type=gettext/ini "$file"
done
mv desktop/*.desktop.in.h po/

echo
echo "*** Creating samsung-tools.pot..."
xgettext -k_ -kN_ -o po/messages.pot `cat po/FILES` po/*.glade.h po/*.desktop.in.h
cat po/messages.pot | sed s:charset=CHARSET:charset=UTF-8: > po/samsung-tools.pot

echo
echo "*** Removing unneeded files..."
rm po/*.glade.h
rm po/*.desktop.in.h
rm po/messages.pot

for locale in `cat po/LINGUAS`; do
	if [ -f po/$locale.po ]; then
		echo "*** Updating '`echo $locale.po | cut -d/ -f2`'..."
		msgmerge -U po/$locale.po po/samsung-tools.pot --backup=off
	else
		echo "*** Creating new '`echo $locale.po | cut -d/ -f2`'..."
		cp po/samsung-tools.pot po/$locale.po
	fi
done