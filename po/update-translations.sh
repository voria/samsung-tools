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

echo
for file in po/*.po; do
	echo "*** Updating '$file'..."
	msgmerge -U "$file" po/messages.pot
done

echo
echo "Done."
