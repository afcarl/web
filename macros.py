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
# To configure, play around in ref_style and bib_entry_style for
# the inline and per line bibliography appearance.
#
# ref_html and bib_entry_html define the html to be used for the
# citation and the bibliography, so look in those to change any
# hyperlinking.

# This is the bibtex file with all of your references in.
BIBFILE = '/home/eeaol/papers/library.bib'

def hook_preconvert_citations():
    """Replace [#citekey] with html"""
    for p in pages:
        # if hasattr(p, 'bibliography'):
        citekeys = list_citekeys(p.source)
        p.citekeys = citekeys
        p.source = replace_all(p.citekeys, p.source)

def bibliography():
    """Create the bibliography"""
    # page.citekeys has been set in the hook_preconvert
    return bib_html(page.citekeys)

def ref_style():
    """Define the in-text citation style"""
    # author, name
    rs = "({author}, {year})"
    # numbered citations
    # rs = "[{cite_no}]"
    return rs

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

def ref_html(citekey, cite_no=None):
    """The html that goes in the text for a given citekey.
    cite_no is used if we're having numbered citations"""
    # dictionary of cite_fields, e.g. author, year, journal,
    cite_fields = gen_citefields(citekey)
    # need this for numbered citations
    if cite_no:
        cite_fields['cite_no'] = cite_no
    ref_text = ref_style().format(**cite_fields)
    link_title = '{author}, {year}'.format(**cite_fields)
    rh = """<a class="citation"
            href="#{citekey}"
            title="{link_title}">{ref_text}
            <span class="citekey"
                    style="display:none">
                    {citekey}
                </span>
            </a>"""
    return rh.format(ref_text=ref_text, citekey=citekey, link_title=link_title)

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

def list_citekeys(text):
    """Create a non duplicating, ordered list of the citekeys found
    in a text.

    TODO: work with citet.
    TODO: work with multiple
    """
    citekey_regex = "\[#(.*?)\]"
    regex = re.compile(citekey_regex)
    citekeys = regex.findall(text)
    # remove duplicates and preserve order
    citekeys = [v for i, v in enumerate(citekeys) if citekeys.index(v) == i]
    return citekeys

def replace(citekey, cite_html, text):
    """Replace citekey with cite_html in text.

    TODO: replace citet as well.
    """
    citekey_regex = "\[#{citekey}\]".format(citekey=citekey)
    regex = re.compile(citekey_regex)
    subbed_text = regex.sub(cite_html, text)
    return subbed_text

def replace_all(citekeys, text):
    for cite_no, citekey in enumerate(citekeys):
        cite_html = ref_html(citekey, cite_no + 1)
        text = replace(citekey, cite_html, text)
    return text
#-----------------------------------------------------------------------------#
