BEGIN {
  found = 0
}

/<a href=\"dblp-20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].xml.gz\">(.*)<\/a>/{
  if (found == 0) {
    matched = match($6, />(.*)<\/a>/)
    if (matched > 0) {
      matched++
      str = substr($6, matched);
      end = index(str, "<");
      ent = substr($6, matched, end-1);
      print ent
      found = 1
    }
  }
}