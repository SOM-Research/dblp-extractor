BEGIN {
}

/><|> <|>  </ {
    do {
        # change the current line
        beg = match($0, "><|> <|>  <");
        if (beg > 0) {
            str = substr($0, beg);
            end = index(str, "<");
            ent = substr($0, beg, end);
            gsub(ent, ">\n<");
            continue;
        }
        break;
    } while (1);
}

{
  print $0;
}