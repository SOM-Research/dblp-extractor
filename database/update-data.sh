#!/bin/sh

echo "start import /data/formatted/www/www_1.xml"

psql -U postgres -f database/incrementality-data.sql -v v1='/data/formatted/update/news.xml'
