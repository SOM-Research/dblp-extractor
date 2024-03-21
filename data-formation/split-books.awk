BEGIN{
is_first_line_printed = 0
is_first_line = 0

f_b_authors = "./data/formatted/book/book-publication.xml";
f_b_editors = "./data/formatted/book/book-p-group.xml";

  f = f_b_authors;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
  f = f_b_editors;
  print "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>" > f
  print "<db>" > f;
}

/<book /{
  is_first_line_printed = 0
  is_first_line = 1
  saveline = $0
  if (match($0, /<book /)){
    firstline = saveline
    $0 = saveline
  }
}

/<editor/{
  is_first_line = 0
  saveline = $0
  if (match($0, /<editor/)){
    f = f_b_editors;
    $0 = saveline
  }
  c++;
}

/<author/{
  is_first_line = 0
  saveline = $0
  if (match($0, /<author/)){
    f = f_b_authors;
    $0 = saveline
  }
  c++;
}

c {
  if (is_first_line == 0) {
    if (is_first_line_printed == 0) {
            print firstline > f
            print $0 > f
            is_first_line_printed = 1
    } else {
        print $0 > f
    }
    }
}

END {
  f = f_b_authors
  print "</db>" > f;
  close(f);
  f = f_b_editors
  print "</db>" > f;
  close(f);
}