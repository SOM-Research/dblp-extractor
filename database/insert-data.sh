#!/bin/sh

psql -U postgres -f database/dbDDL.sql

echo "start import /data/formatted/www/www_1.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_1.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_2.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_2.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_3.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_3.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_4.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_4.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_5.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_5.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_6.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_6.xml' -v v2="'www'"
echo "start import /data/formatted/www/www_7.xml"
psql -U postgres -f database/importer-researchers.sql -v v1='/data/formatted/www/www_7.xml' -v v2="'www'"

rm /data/formatted/www/www_1.xml
rm /data/formatted/www/www_2.xml
rm /data/formatted/www/www_3.xml
rm /data/formatted/www/www_4.xml
rm /data/formatted/www/www_5.xml
rm /data/formatted/www/www_6.xml
rm /data/formatted/www/www_7.xml

echo "start import /data/formatted/proceedings/proceedings.xml"
psql -U postgres -f database/importer-publication-venues-and-groups.sql -v v1='/data/formatted/proceedings/proceedings.xml' -v v2="'proceedings'" -v v3="'//proceedings'"
rm /data/formatted/proceedings/proceedings.xml

echo "start import /data/formatted/book/book-p-group.xml"
psql -U postgres -f database/importer-publication-venues-and-groups.sql -v v1='/data/formatted/book/book-p-group.xml' -v v2="'book'" -v v3="'//book'"
rm /data/formatted/book/book-p-group.xml
echo "start import /data/formatted/book/book-publication.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/book/book-publication.xml' -v v2="'book'" -v v3="'//book'"
rm /data/formatted/book/book-publication.xml

echo "start import /data/formatted/mastersthesis/mastersthesis.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/mastersthesis/mastersthesis.xml' -v v2="'mastersthesis'" -v v3="'//mastersthesis'"
rm /data/formatted/mastersthesis/mastersthesis.xml

echo "start import /data/formatted/data/data.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/data/data.xml' -v v2="'data'" -v v3="'//data'"
rm /data/formatted/data/data.xml

echo "start import /data/formatted/phdthesis/phdthesis.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/phdthesis/phdthesis.xml' -v v2="'phdthesis'" -v v3="'//phdthesis'"
rm /data/formatted/phdthesis/phdthesis.xml

echo "start import /data/formatted/incollection/incollection.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/incollection/incollection.xml' -v v2="'incollection'" -v v3="'//incollection'"
rm /data/formatted/incollection/incollection.xml

echo "start import /data/formatted/article/article_1.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_1.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_2.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_2.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_3.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_3.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_4.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_4.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_5.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_5.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_6.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_6.xml' -v v2="'article'" -v v3="'//article'"
echo "start import /data/formatted/article/article_7.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/article/article_7.xml' -v v2="'article'" -v v3="'//article'"
rm /data/formatted/article/article_1.xml
rm /data/formatted/article/article_2.xml
rm /data/formatted/article/article_3.xml
rm /data/formatted/article/article_4.xml
rm /data/formatted/article/article_5.xml
rm /data/formatted/article/article_6.xml
rm /data/formatted/article/article_7.xml

echo "start import /data/formatted/inproceedings/inproceedings_1.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_1.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_2.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_2.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_3.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_3.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_4.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_4.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_5.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_5.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_6.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_6.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
echo "start import /data/formatted/inproceedings/inproceedings_7.xml"
psql -U postgres -f database/importer-publications.sql -v v1='/data/formatted/inproceedings/inproceedings_7.xml' -v v2="'inproceedings'" -v v3="'//inproceedings'"
rm /data/formatted/inproceedings/inproceedings_1.xml
rm /data/formatted/inproceedings/inproceedings_2.xml
rm /data/formatted/inproceedings/inproceedings_3.xml
rm /data/formatted/inproceedings/inproceedings_4.xml
rm /data/formatted/inproceedings/inproceedings_5.xml
rm /data/formatted/inproceedings/inproceedings_6.xml
rm /data/formatted/inproceedings/inproceedings_7.xml

echo "start insert relationships and insert institutions"
psql -U postgres -f database/importer-relationships-many-to-many.sql

echo "Add countries in institutions"
psql -U postgres -f database/add_country.sql

echo "start update publications add num_pages"
psql -U postgres -f database/number-pages-publications.sql
