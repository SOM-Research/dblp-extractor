#!/bin/sh

echo "start import /data/formatted/www/www_1.xml"

psql -U postgres -f database/incrementality-data.sql -v v1='/data/formatted/update/news.xml'

echo "start insert relationships and insert institutions"
psql -U postgres -f database/update-relationships-many-to-many.sql

#echo "Add countries in institutions"
#psql -U postgres -f database/add_country.sql

echo "start update publications add num_pages"
psql -U postgres -f database/number-pages-publications.sql
