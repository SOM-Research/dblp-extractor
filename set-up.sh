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

last_release="dblp-2024-03-01.xml.gz"
gzip -d ./data/$last_release

echo "DBLP xml downloaded and uncompressed"

: '
Create directories to save split xml
'
mkdir -p ./data/formatted/article
mkdir -p ./data/formatted/book
mkdir -p ./data/formatted/incollection
mkdir -p ./data/formatted/inproceedings
mkdir -p ./data/formatted/mastersthesis
mkdir -p ./data/formatted/phdthesis
mkdir -p ./data/formatted/proceedings
mkdir -p ./data/formatted/www
mkdir -p ./data/formatted/data

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

gawk -f ./data-formation/spacemaker.awk ./data/$dblp_xml > ./data/$dblp_spaced
echo "Xml  ./data/$dblp_spaced DONE"
gawk -f ./data-formation/parser.awk ./data/$dblp_spaced > ./data/$dblp_parsed
echo "Xml  ./data/$dblp_parsed DONE"
gawk -f ./data-formation/split.awk ./data/$dblp_parsed
echo "Xml split DONE"

: '
Remove unused xml
'
rm ./data/$dblp_xml
echo "Xml ./data/$dblp_xml REMOVED DONE"
rm ./data/$dblp_spaced
echo "Xml ./data/$dblp_spaced REMOVED DONE"
rm ./data/$dblp_parsed
echo "Xml ./data/$dblp_parsed REMOVED DONE"

: '
Split big xml files in batches more workeable files
'
: '
WWW file (Researchers) divided in 500000 items per file expecting a total of 7 files
'

gawk -v maxRecs=500000 -v RS='</www>\n' -v ORS= '
    (NR % maxRecs) == 1 {
        close(out); out="./data/formatted/www/small_www_" (++fileNr) ".xml"
    }
    RT { print $0 RT > out }
' data/formatted/www/www.xml

echo "Splited www."

sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_1.xml data/formatted/www/www_1.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_2.xml data/formatted/www/www_2.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_3.xml data/formatted/www/www_3.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_4.xml data/formatted/www/www_4.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_5.xml data/formatted/www/www_5.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_6.xml data/formatted/www/www_6.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/www/small_www_7.xml data/formatted/www/www_7.xml

echo "Reformate small www."


: '
Article file (Publications) divided in 500000 items per file expecting a total of 7 files
'

gawk -v maxRecs=500000 -v RS='</article>\n' -v ORS= '
    (NR % maxRecs) == 1 {
        close(out); out="./data/formatted/article/small_article_" (++fileNr) ".xml"
    }
    RT { print $0 RT > out }
' data/formatted/article/article.xml

echo "Splited article."

sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_1.xml data/formatted/article/article_1.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_2.xml data/formatted/article/article_2.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_3.xml data/formatted/article/article_3.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_4.xml data/formatted/article/article_4.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_5.xml data/formatted/article/article_5.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_6.xml data/formatted/article/article_6.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/article/small_article_7.xml data/formatted/article/article_7.xml

echo "Reformate small article."

: '
WWW file (Researchers) divided in 500000 items per file expecting a total of 7 files
'

gawk -v maxRecs=500000 -v RS='</inproceedings>\n' -v ORS= '
    (NR % maxRecs) == 1 {
        close(out); out="./data/formatted/inproceedings/small_inproceedings_" (++fileNr) ".xml"
    }
    RT { print $0 RT > out }
' data/formatted/inproceedings/inproceedings.xml

echo "Splited inproceedings."

sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_1.xml data/formatted/inproceedings/inproceedings_1.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_2.xml data/formatted/inproceedings/inproceedings_2.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_3.xml data/formatted/inproceedings/inproceedings_3.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_4.xml data/formatted/inproceedings/inproceedings_4.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_5.xml data/formatted/inproceedings/inproceedings_5.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_6.xml data/formatted/inproceedings/inproceedings_6.xml
sh data-formation/reformate-files-split-in-batches.sh data/formatted/inproceedings/small_inproceedings_7.xml data/formatted/inproceedings/inproceedings_7.xml

echo "Reformate small inproceedings."

: '
book file (publications and publication groups) divided by have authors or editors
that means are publication or publication groups respectively
'

gawk -f ./data-formation/split-books.awk

echo "Splited books in p-group books and publication books"

: '
Remove small xmls.
'

 rm data/formatted/*/small*.xml

: '
Build and run Docker containers
'

echo "Run dockers: "

docker compose build
docker compose up -d

: '
To insert data to database we should execute set-up-database.sh from postgres docker container.
'
echo "insert data inside db container"
docker compose exec -d db sh database/insert-data.sh

: '
Finally we are going to up the python project with their requirements. (TO DO)
'

echo "DONE"