#!/usr/bin/awk -f
#
# Usage:
#
#     ./replace-html-entities.awk replace-html-entities.input.html > replace-html-entities.output.html
#
# Author: Fabio Lima
# Date: 2023-04-23
#
#     ./parser.awk test.xml > test-fix.xml
#

BEGIN {
    ENT["&Agrave;"]= "À" 
    ENT["&Aacute;"]= "Á"
    ENT["&Acirc;"]= "Â"
    ENT["&Atilde;"]= "Ã"
    ENT["&Auml;"]= "Ä"
    ENT["&Aring;"]= "Å"
    ENT["&agrave;"]= "à"
    ENT["&aacute;"]= "á"
    ENT["&acirc;"]= "â"
    ENT["&atilde;"]= "ã"
    ENT["&auml;"]= "ä"
    ENT["&aring;"]= "å"
    ENT["&Egrave;"]= "È"
    ENT["&Eacute;"]= "É"
    ENT["&Ecirc;"]= "Ê"
    ENT["&Euml;"]= "Ë"
    ENT["&egrave;"]= "è"
    ENT["&eacute;"]= "é"
    ENT["&ecirc;"]= "ê"
    ENT["&euml;"]= "ë"
    ENT["&Igrave;"]= "Ì"
    ENT["&Iacute;"]= "Í"
    ENT["&Icirc;"]= "Î"
    ENT["&Iuml;"]= "Ï"
    ENT["&igrave;"]= "ì"
    ENT["&iacute;"]= "í"
    ENT["&icirc;"]= "î"
    ENT["&iuml;"]= "ï"
    ENT["&Ograve;"]= "Ò"
    ENT["&Oacute;"]= "Ó"
    ENT["&Ocirc;"]= "Ô"
    ENT["&Otilde;"]= "Õ"
    ENT["&Ouml;"]= "Ö"
    ENT["&ograve;"]= "ò"
    ENT["&oacute;"]= "ó"
    ENT["&ocirc;"]= "ô"
    ENT["&otilde;"]= "õ"
    ENT["&ouml;"]= "ö"
    ENT["&Ugrave;"]= "Ù"
    ENT["&Uacute;"]= "Ú"
    ENT["&Ucirc;"]= "Û"
    ENT["&Uuml;"]= "Ü"
    ENT["&ugrave;"]= "ù"
    ENT["&uacute;"]= "ú"
    ENT["&ucirc;"]= "û"
    ENT["&uuml;"]= "ü"

    ENT["&Yacute;"]= "Ý"
    ENT["&159;"]= "Ÿ"
    ENT["&yacute;"]= "ý"
    ENT["&yuml;"]= "ÿ"

    ENT["&AElig;"]= "Æ"
    ENT["&aelig;"]= "æ"
    ENT["&szlig;"]= "ß"
    ENT["&Ccedil;"]= "Ç"
    ENT["&ccedil;"]= "ç"
    ENT["&Ntilde;"]= "Ñ"
    ENT["&ntilde;"]= "ñ"
    ENT["&Oslash;"]= "Ø"
    ENT["&oslash;"]= "ø"
    ENT["&micro;"]= "µ"
    ENT["&reg;"]= "®"
    ENT["&times;"]= "⊗"
    ENT["&eth;"]= "ð"
    ENT["&ETH;"]= "Ð"
    ENT["&THORN;"]= "Þ"
    ENT["&thorn;"]= "þ"

    ENT["&#131;"]= "ƒ"
    ENT["&#140;"]= "Œ"
    ENT["&#156;"]= "œ"
    ENT["&#138;"]= "Š"
    ENT["&#154;"]= "š"
    ENT["&#181;"]= "µ"
    ENT["&#215;"]= "×"
}

/&[^;]+;/ {
    do {
        # change the current line
        beg = match($0, "&[^;]+;");
        if (beg > 0) {
            str = substr($0, beg);
            end = index(str, ";");
            ent = substr($0, beg, end);
            gsub(ent, ENT[ent]);
            continue;
        }
        break;
    } while (1);
}

{
    # append current line
    #output=output $0 "\\n";
    print  $0;
}

END {
    # escape percent char
    #gsub("%", "%%", output);

    # System PRINTF for \uFFFF \UFFFFFFFF
    # AWK's PRINTF don't support Unicode
    #system("/usr/bin/printf '"output"'");
}

# SOURCE: https://gist.github.com/fabiolimace/4bfac9c7dafa3a3114b64a9b3e9725b6#file-replace-html-entities-awk