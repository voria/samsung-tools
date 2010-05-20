#!/bin/bash
# This script is intended to be called from Makefile, it prepares .desktop files
# It's a bit hackish but it works

FILE="$1"
NEWFILE=`echo $FILE | sed 's:.in::'`

# Get the translatable strings
NAME=`grep ^_Name "$FILE" | cut -d= -f2`
COMMENT=`grep ^_Comment "$FILE" | cut -d= -f2`

# Remove the underscores and create the new .desktop file
cat $FILE | sed 's:_Name:Name:' | sed 's:_Comment:Comment:' > $NEWFILE

# Add translations for "Name="
if [ -n "$NAME" ]; then
	# For each language specified in po/LINGUAS, take the translation from the .po file and
	# add it to the new .desktop file as Name[language]
	for lang in `cat po/LINGUAS`; do
		TRANSLATION=`msggrep --msgid -F -e "$NAME" po/$lang.po | tac | sed -n '1p' | cut -d\" -f 2`
		if [ -n "$TRANSLATION" ]; then
			echo -n "Name[$lang]=" >> $NEWFILE
			echo "$TRANSLATION" >> $NEWFILE
		fi
	done
fi

# Add translations for "Comment="
if [ -n "$COMMENT" ]; then
	# For each language specified in po/LINGUAS, take the translation from the .po file and
	# add it to the new .desktop file as Comment[language]
	for lang in `cat po/LINGUAS`; do
		TRANSLATION=`msggrep --msgid -F -e "$COMMENT" po/$lang.po | tac | sed -n '1p' | cut -d\" -f 2`
		if [ -n "$TRANSLATION" ]; then
			echo -n "Comment[$lang]=" >> $NEWFILE
			echo "$TRANSLATION" >> $NEWFILE
		fi
	done
fi
