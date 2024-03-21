#!/bin/sh
echo "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" >> $2
echo "<db>" >> $2
awk '{ print $0 }' $1 >> $2
echo "</db>" >> $2