#!/bin/sh
CURL="/usr/bin/curl"
dblp_url="https://dblp.org/xml/release/"

: '
We are going to download dblp xml and uncompress it.
'

last_release=$($CURL $dblp_url | awk -f ./data-formation/last-dblp-xml.awk )
echo "last release is: $last_release"
last_release_url="$dblp_url$last_release"
echo "last release URL is: $last_release_url"
$CURL $last_release_url > ./data/$last_release
gzip -d ./data/$last_release

echo "DBLP xml downloaded and uncompressed"

: '
Create directories to save split xml
'
mkdir -p ./data/formatted/article
mkdir -p ./data/formatted/book
mkdir -p ./data/formatted/incollection
mkdir -p ./data/formatted/inproceedings
mkdir -p ./data/formatted/masterthesis
mkdir -p ./data/formatted/phdthesis
mkdir -p ./data/formatted/proceedings
mkdir -p ./data/formatted/www

: '
Then we are formatting and splitting the xml.
The order of awk executions are:
- spacemaker
- parser
- split
The spacemaker creates a break line between xml items, the parser substitutes the "strange" characters to
more readible ones and the split splits the xml in 8 different xml documents by item.
The spacemaker and the parser could execute in different order but the split must be the last one to be
executed, otherwise we should execute the other awks for each xml split.
'
dblp_xml=${last_release%".gz"}
dblp_spaced="dblp_spaced.xml"
dblp_parsed="dblp_parsed.xml"

echo "Spaced = ./data/$dblp_spaced"
echo "Parsed = ./data/$dblp_parsed"

awk -f ./data-formation/spacemaker.awk ./data/$dblp_xml > ./data/$dblp_spaced
awk -f ./data-formation/parser.awk ./data/$dblp_spaced > ./data/$dblp_parsed
awk -f ./data-formation/split.awk ./data/$dblp_parsed

echo "DBLP xml formatted and split"

: '
To insert data to database we should execute set-up-database.sh from postgres docker container.
'

: '
Finally we are going to up the python project with their requirements. (TO DO)
'

echo "DONE"