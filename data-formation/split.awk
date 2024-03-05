BEGIN{
  n = 0
  c = 0

  itemcount_article = 0
  itemcount_www = 0
  itemcount_book = 0
  itemcount_proceedings = 0
  itemcount_inproceedings = 0
  itemcount_mastersthesis = 0
  itemcount_phdthesis = 0
  itemcount_incollection = 0

  n_article = 0
  n_www = 0
  n_book = 0
  n_proceedings = 0
  n_inproceedings = 0
  n_mastersthesis = 0
  n_phdthesis = 0
  n_incollection = 0

  f_article = "../data/formatted/article/article.xml";
  f_www = "../data/formatted/www/www.xml";
  f_book = "../data/formatted/book/book.xml";
  f_proceedings = "../data/formatted/proceedings/proceedings.xml";
  f_inproceedings = "../data/formatted/inproceedings/inproceedings.xml";
  f_mastersthesis = "../data/formatted/mastersthesis/mastersthesis.xml";
  f_phdthesis = "../data/formatted/phdthesis/phdthesis.xml";
  f_incollection = "../data/formatted/incollection/incollection.xml";


  f = f_article;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_www;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_book;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_proceedings;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_inproceedings;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_mastersthesis;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_phdthesis;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_incollection;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;



}

/<article /{
  f = f_article;
  saveline = $0
  if (match($0, /<article /)){
    itemcount_article++;
    $0 = saveline
  }
  c++;
}

/<www /{
  f = f_www;
  saveline = $0
  if (match($0, /<www /)){
    itemcount_www++;
    $0 = saveline
  }
  c++;
}

/<book /{
  f = f_book;
  saveline = $0
  if (match($0, /<book /)){
    itemcount_book++;
    $0 = saveline
  }
  c++;
}

/<proceedings /{
  f = f_proceedings;
  saveline = $0
  if (match($0, /<proceedings /)){
    itemcount_proceedings++;
    $0 = saveline
  }
  c++;
}

/<inproceedings /{
  f = f_inproceedings;
  saveline = $0
  if (match($0, /<inproceedings /)){
    itemcount_inproceedings++;
    $0 = saveline
  }
  c++;
}

/<mastersthesis /{
  f = f_mastersthesis;
  saveline = $0
  if (match($0, /<mastersthesis /)){
    itemcount_mastersthesis++;
    $0 = saveline
  }
  c++;
}

/<phdthesis /{
  f = f_phdthesis;
  saveline = $0
  if (match($0, /<phdthesis /)){
    itemcount_phdthesis++;
    $0 = saveline
  }
  c++;
}

/<incollection /{
  f = f_incollection;
  saveline = $0
  if (match($0, /<incollection /)){
    itemcount_incollection++;
    $0 = saveline
  }
  c++;
}

c {
if ($0 != "</list>") {
  print $0 > f
}
}

END {
  f = f_article
  print "</db>" > f;
  close(f);

  f = f_www
  print "</db>" > f;
  close(f);

  f = f_book
  print "</db>" > f;
  close(f);

  f = f_proceedings
  print "</db>" > f;
  close(f);

  f = f_inproceedings
  print "</db>" > f;
  close(f);

  f = f_mastersthesis
  print "</db>" > f;
  close(f);

  f = f_phdthesis
  print "</db>" > f;
  close(f);

  f = f_incollection
  print "</db>" > f;
  close(f);

  print itemcount_article
  print itemcount_www
  print itemcount_book
  print itemcount_proceedings
  print itemcount_inproceedings
  print itemcount_mastersthesis
  print itemcount_phdthesis
  print itemcount_incollection
}