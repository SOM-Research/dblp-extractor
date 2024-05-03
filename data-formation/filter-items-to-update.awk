BEGIN {
  last_date = v_last_date
  itemcount_news = 0
  itemcount_olds = 0
  f_news = "./data/formatted/update/news.xml";
  f_olds = "./data/formatted/update/olds.xml";
  f = f_news;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_olds;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
}

/ mdate="[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]"/{
  saveline = $0
  item_date = substr($2, 8, 10)
  if (item_date > last_date) {
    itemcount_news++;
    f = f_news
  }
  if (item_date <= last_date) {
    itemcount_olds++;
    f = f_olds
  }
  $0 = saveline
  c++;
}

c {
  print $0 > f
}


END {
  f = f_news
  print "</db>" > f;
  close(f);
  f = f_olds
  print "</db>" > f;
  close(f);

  f = "./data/formatted/count-items-update.txt";
  print sprintf("news: %d", itemcount_news) > f
  print sprintf("olds: %d", itemcount_olds) > f
}