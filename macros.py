try:
    from pybtex.database.input.bibtex import Parser
except ImportError:
    print("No bibliography support")

import re
from datetime import datetime
import os.path


_SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
"""

_SITEMAP_URL = """
<url>
    <loc>%s/%s</loc>
    <lastmod>%s</lastmod>
    <changefreq>%s</changefreq>
    <priority>%s</priority>
</url>
"""


def hook_preconvert_sitemap():
    """Generate Google sitemap.xml file."""
    date = datetime.strftime(datetime.now(), "%Y-%m-%d")
    urls = []
    for p in pages:
        urls.append(_SITEMAP_URL % (options.base_url.rstrip('/'), p.url, date,
                    p.get("changefreq", "monthly"), p.get("priority", "0.8")))
    fname = os.path.join(options.project, "output", "sitemap.xml")
    fp = open(fname, 'w')
    fp.write(_SITEMAP % "".join(urls))
    fp.close()


#-------------------------------CITATIONS----------------------#
# This is a big hack. It is reliant on pybtex being available to
# do the bibtex parsing. It will break if you try and reference
# things that don't have the appropriate bibtex entries.
#
# TODO: handle exceptions.
#       - missing pybtex
#       - missing bibfile
#       - missing citation fields
# TODO: find and render citet ([#key;]
# TODO: find multiple citations ([#key1, key2])
#
# Aaron O'Leary Nov 2012
#
# To configure, play around in make_ref_html and bib_entry_style for
# the inline and per line bibliography appearance.
#
# make_ref_html and bib_entry_html define the html to be used for the
# citation and the bibliography, so look in those to change any
# hyperlinking.

# This is the bibtex file with all of your references in.
BIBFILE = '/home/eeaol/papers/library.bib'


def hook_preconvert_citations():
    """Replace [#citekey] with html"""
    for p in pages:
        citekeys = list_unique_citekeys(p.source)
        p.citekeys = citekeys
        matches = list_citematches(p.source)
        p.source = replace_all(matches, p.source)


def bibliography():
    """Create the bibliography"""
    # page.citekeys has been set in the hook_preconvert
    return bib_html(page.citekeys)


def ref_style(style='citep'):
    """Define the in-text citation style"""
    # author, name
    if style is 'citep':
        return "{author}, {year}"
    elif style is 'citet':
        return "{author} ({year})"
    elif style is 'numbered':
        return "[{cite_no}]"


def bib_entry_style():
    """The text that goes in the references for a given citekey."""
    bs = "{authors}, \
        <strong>{title}</strong>, \
        <em>{journal}</em>, {year}"
    return bs


#---------------CITATION methods ---------------------------------------------#
def load_citekey(citekey, bibfile=BIBFILE):
    """ Get the info corresponding to specific citekey
    from bibfile.
    """
    parser = Parser()
    bib_data = parser.parse_file(bibfile)
    entry = bib_data.entries[citekey]
    return entry


def gen_citefields(citekey):
    """Rearrange the bib entries into something more useful.
    The programmatic interation with Pybtex is very poorly
    documented, making this necessary.
    """
    entry = load_citekey(citekey)
    D = entry.fields
    authors = [" ".join(p.last()) for p in entry.persons['author']]
    D['authors'] = ", ".join(authors)
    if len(authors) == 1:
        D['author'] = authors[0]
    elif len(authors) == 2:
        D['author'] = " and ".join(authors[0:2])
    elif len(authors) > 2:
        D['author'] = authors[0] + ' et al'
    return D


def make_ref_html(match):
    """From a mmd citation element, create the appropriate html
    replacement.

    the text replacement should go as

    key        --> (author, year)                   (citep)
    key;       --> author (year)                    (citet)
    key, key2  --> (author, year; author2, year2)   (citep)
    key, key2; --> author (year); author2, (year2)  (citet)
    """
    def make_key_html(citekey, style):
            """Make the html for a single citekey, with given cite
            style (e.g. 'citet', 'citep').
            """
            cite_fields = gen_citefields(citekey)
            link_title = '{journal}'.format(**cite_fields)
            ref_html_skeleton = ('<a class="citation" '
                                 'href="#{citekey}"'
                                 'title="{link_title}">'
                                 '{ref_text}'
                                 '<span class="citekey" '
                                 'style="display:none">'
                                 '{citekey}'
                                 '</span>'
                                 '</a>')
            ref_text = ref_style(style).format(**cite_fields)
            return ref_html_skeleton.format(ref_text=ref_text,
                                            citekey=citekey,
                                            link_title=link_title)

    if match[-1] != ';':
        # citep
        citekeys = match.split(', ')
        ref_htmls = [make_key_html(key, style='citep') for key in citekeys]
        ref_html = '(' + '; '.join(ref_htmls) + ')'
        return ref_html
    elif match[-1] == ';':
        # citet
        citekeys = match[:-1].split(', ')
        ref_htmls = [make_key_html(key, style='citet') for key in citekeys]
        ref_html = '; '.join(ref_htmls)
        return ref_html


def bib_entry_html(citekey):
    """The html that goes in the references for a given citekey."""
    cite_fields = gen_citefields(citekey)
    bib_entry_text = bib_entry_style().format(**cite_fields)
    beh = """<li id={citekey} class="citation">
            <span class="citekey"
                    style="display:none">
                    {citekey}
            </span>
            <p> {bib_entry_text}
            <a href={link_to_paper}> Get the paper </a>
            </p>
            </li>
        """
    link = "http://homepages.see.leeds.ac.uk/~eeaol/p/{}.pdf".format(citekey)
    return beh.format(citekey=citekey,
                      bib_entry_text=bib_entry_text,
                      link_to_paper=link)


def bib_html(citekeys):
    """The entire html of the reference section"""
    bib_entries = "".join(map(bib_entry_html, citekeys))
    bibh = """<div class="bibliography">
            <ol>
                {bib_entries}
            </ol>
            </div>
            """
    return bibh.format(bib_entries=bib_entries)


def list_citematches(text):
    """List all mmd citation matches."""
    # all mmd citations regardless of type (keeping ; that tells us
    # citet / citep)
    all_regex = "\[#(.*?)\]"
    all_match_re = re.compile(all_regex)
    all_matches = all_match_re.findall(text)
    return all_matches


def list_unique_citekeys(text):
    """Creates a unique list of citation keys/

    We could find specific keys with these:

        # cite p end is not preceded by a ;
        citep_regex = "\[#(.*?)(?<!;)\]"
        # cite t end is preceded by a ;
        citet_regex = "\[#(.*?);\]"
        # all keys regardless of type
        all_regex = "\[#(.*?);?\]"
    """
    # find all mmd citations regardless of type
    all_regex = "\[#(.*?);?\]"
    all_ = re.compile(all_regex)
    all_keys_with_multiple = all_.findall(text)
    # split multiples
    all_keys = [s.split(', ') for s in all_keys_with_multiple]
    # flatten lists
    flat_all_keys = [i for sub in all_keys for i in sub]
    # remove duplicates and preserve order
    citekeys = [v for i, v in enumerate(flat_all_keys)
                if flat_all_keys.index(v) == i]
    return citekeys


def replace_all(matches, text):
    for match in matches:
        cite_html = make_ref_html(match)
        # something to allow verbatim here?
        mmd_cite_element = '\[#{key}\]'.format(key=match)
        regex = re.compile(mmd_cite_element)
        # replace the match with appropriate html
        text = regex.sub(cite_html, text)
    return text
#-----------------------------------------------------------------------------#
