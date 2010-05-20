#!/bin/bash
# This script is intended to be called from Makefile, it prepares .server files
# It's a bit hackish but it works

FILE="$1"
NEWFILE=`echo $FILE | sed 's:.in::'`

# Get the translatable string
VALUE=`grep _value "$FILE" | sed 's:.*_value=::' | cut -d\" -f2`

# The line where the translatable string has been found
VALUELINE=`grep _value "$FILE"`

# Remove the underscore and create the first part of the new .server file
sed -n '1,/.*_value/p' "$FILE" | sed 's/_value/value/' > $NEWFILE

# Add translations
if [ -n "$VALUE" ]; then
	# For each language specified in po/LINGUAS, take the translation from the .po file and
	# add it to the new .server file
	for lang in `cat po/LINGUAS`; do
		TRANSLATION=`msggrep --msgid -F -e "$VALUE" po/$lang.po | tac | sed -n '1p' | cut -d\" -f 2`
		if [ -n "$TRANSLATION" ]; then
			echo "$VALUELINE" | sed "s/description/description-$lang/" | sed "s/_value/value/" | sed "s/$VALUE/$TRANSLATION/" >> $NEWFILE
		fi
	done
fi

# Write the remaining part of the .server file
sed -n '/.*_value/,/END/p' "$FILE" | sed -n '2,/END/p' >> $NEWFILE