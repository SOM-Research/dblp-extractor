#!/bin/sh
CURL="/usr/bin/curl"
dblp_url="https://dblp.org/xml/release/"

: '
We are going to download dblp xml and uncompress it.
'

last_release=$($CURL $dblp_url | awk -f ./data-formation/last-dblp-xml.awk)
echo "last release is: $last_release"
last_release_url="$dblp_url$last_release"
echo "last release URL is: $last_release_url"

$CURL $last_release_url > ./data/$last_release
gzip -d ./data/$last_release

echo "DBLP xml downloaded and uncompressed"

mkdir -p ./data/formatted/update

mkdir -p ./data/formatted/article
mkdir -p ./data/formatted/book
mkdir -p ./data/formatted/incollection
mkdir -p ./data/formatted/inproceedings
mkdir -p ./data/formatted/mastersthesis
mkdir -p ./data/formatted/phdthesis
mkdir -p ./data/formatted/proceedings
mkdir -p ./data/formatted/www
mkdir -p ./data/formatted/data



dblp_xml=${last_release%".gz"}
dblp_spaced="dblp_spaced.xml"
dblp_parsed="dblp_parsed.xml"


echo "Xml  ./data/$dblp_xml"
gawk -f ./data-formation/spacemaker.awk ./data/$dblp_xml > ./data/formatted/update/$dblp_spaced
echo "Xml  ./data/formatted/update/$dblp_spaced DONE"
gawk -f ./data-formation/parser.awk ./data/formatted/update/$dblp_spaced > ./data/formatted/update/$dblp_parsed
echo "Xml  ./data/formatted/update/$dblp_parsed DONE"


docker compose exec -it db psql -U postgres -d metascience -c "COPY (SELECT xml_mdate::text FROM publications UNION (SELECT xml_mdate::text FROM researchers) UNION (SELECT xml_mdate::text FROM publication_groups) ORDER BY xml_mdate DESC LIMIT 1) TO '/data/last_date.txt' ;"
last_date=$(<./data/last_date.txt)


gawk -f ./data-formation/filter-items-to-update.awk -v v_last_date=$last_date ./data/formatted/update/$dblp_parsed



