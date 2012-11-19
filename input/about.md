date: 06/03/2012
---

I really didn't want to write any html for this site. Html is horrible.
I know and use [Markdown][md] and just needed something to manage my Markdown
content.

[md]: http://daringfireball.net/projects/markdown/

Trying to understand [Hyde][] made my head hurt. It was too complicated
for what I need. There are lots of static site generators written in Ruby.
That's no good for me - I understand Python and don't want to spend
time fiddling with ruby.

[Hyde]: http://ringce.com/hyde

I tried to write my own CMS in bash but the complexity quickly builds up 
(beyond the 50 lines of code I limited myself to) when you try and make your
site do anything useful. Whilst reinventing the wheel is good for learning,
it isn't especially efficient. 

A bit more searching and I came across [Poole], which says

>   Poole may be a good choice if you are familiar with Markdown and Python
>   and if you want to build a rather simple site with only a spot of
>   generated content.

[Poole]: https://bitbucket.org/obensonne/poole/overview

Great. I know Markdown and Python and I want a simple site!

### Posts ###

If we want to put posts into the notes section of the site and want
them to appear in the page we need to do a couple of things.

+ file header needs to contain a 'post:' entry
+ file header needs to be terminated by `---`

I don't want to write these into the original notes to keep it clean and
maintain compatibility with multimarkdown.  

This is something that is easily scripted. The idea is that I'll have some
notes written in Markdown somewhere on my machine and then do `webify filename`
and have it appear in the blog section of the website.

`Webify` looks something like this (in bash):

    #!/bin/bash
    filepath=$1
    # file may or may not have .extension
    filename=$(basename ${filepath})
    short_filename=${filename%.*}

    # where is the webpage input dir?
    input_dir=$HOME/web/input/notes

    # get the date from the file, assuming dd/mm/yyyy format and
    # converting to yyyy-mm-dd
    date=$(grep -i -m 1 'date: [0-9]./[0-9]./[0-9]...' $filename |\
            sed -e 's/^[^0-9]*//' \
                -e 's/\(..\)\/\(..\)\/\(....\)/\3-\2-\1/')

    title=$(grep -i -m 1 'title: .*' $filename)

    year=${date:0:4}
    month=${date:5:2}

    newdir=${input_dir}/$year/$month
    mkdir -p $newdir
    newfilepath=$newdir/${short_filename}.md
    cp $filepath $newfilepath

    # remove the old title from the file
    #sed -i '/title:.*/d' $newfilepath
    # remove the old date from the file
    #sed -i '/[Dd]ate: [0-9].\/[0-9].\/[0-9].../d' $newfilepath
    # remove all the metadata from the file (it has to be separated
    # from the content by a blank line)
    sed -i '1,/^$/d' $newfilepath

    # add the metadata to the start of the file
    post=$(echo $short_filename | sed 's/[_-]/ /g')
    echo "$title" >> tmpf
    echo "post: $post" >> tmpf
    echo "date: $date" >> tmpf
    echo -e "---\n" >> tmpf
    cat $newfilepath >> tmpf
    mv tmpf $newfilepath
    rm -f tmpf


### Syntax Highlighting ###

This isn't enabled by default in Poole, but it is easy to get set up.

[CodeHilite][] is an included extension to python-markdown. The only
requirement is [Pygments][].

[CodeHilite]: http://freewisdom.org/projects/python-markdown/CodeHilite
[Pygments]: http://pygments.org/

To get syntax highlighting you need a css for pygment to work with.
Add this to your template page (page.html)

    <link rel="stylesheet" type="text/css" href="style/pygment.css" />
    
and make sure that style contains pygment.css, where this is a file
like one of [these][css-ex]

[css-ex]: https://github.com/icco/pygments-css

with all of the `.highlight` at the start of the lines replaced with
`.codehilite` (as this is the css class that markdown wraps code in),
e.g

    sed -i 's/^\.highlight/.codehilite/g' name_of_pygment_css_file.css

Then build poole with 

    poole --build --md-ext='codehilite(guess_lang=False)'

### Clean URLS ###

This was a bit more hassle, but not that much. In the template page
there is some inline python which creates the menu automatically for
any page that contains "menu-position" metadata. We just need to change
this so that it points to clean urls.

    #!python
    mpages = [p for p in pages if "menu-position" in p]
    mpages.sort(key=lambda p: int(p["menu-position"]))
    entry = '<span class="%s"><a href="%s">%s</a></span>'
    for p in mpages:
        style = p["title"] == page["title"] and "current" or ""
        site_base = "http://homepages.see.leeds.ac.uk/~eeaol/"
        if 'index.html' in p["url"]:
            clean_url = site_base + p["url"].split('index.html')[0]
        else:
            clean_url = p["url"].split('.html')[0] + '/'
        
        print(entry % (style, htmlspecialchars(clean_url), htmlspecialchars(p["title"])))

We also need to modify .htaccess so that apache knows what to do with
the clean urls that it is being passed. The following seems clunky, but
it works.


    #!apache
    RewriteEngine On
    RewriteBase /~eeaol/

    # If there is an index.html in the root of the thing I'm asking
    # for, load it up.
    RewriteCond %{REQUEST_FILENAME}/index.html -f
    RewriteRule ^(.+)/$ $1/index.html [L]

    # If it isn't a file, put a slash on it
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule .*[^/]$ %{REQUEST_URI}/ [L,R=301]

    # If there is a corresponding .html and it isn't a directory,
    # remove the slash and add .html
    RewriteCond %{REQUEST_FILENAME}.html -f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.+)/$ $1.html [L]

This means that directories on the site can be accessed naked
unless they have an index.html in them.

Files on the site with no extension can still be accessed and
a trailing slash will not be added.

Pages can be requested with and without the trailing slash,
but the trailing slash will always be added on.

[More][corz] on [htaccess][]
[corz]: http://corz.org/serv/tricks/htaccess2.php
[htaccess]: http://www.codingforums.com/showthread.php?t=215977

### Makefile ###

I made a makefile for the site to quicken things up. I can easily rebuild the
site with `make build`, then push it out with `make deploy`. Here's the file
anyway:

    #!make
    build: 
        poole --build --md-ext='codehilite' --base-url="http://homepages.see.leeds.ac.uk/~eeaol/"
        cp htaccess output/.htaccess

    test:
        poole --build --md-ext='codehilite' --base-url="/home/eeaol/web/output/"
        cp htaccess output/.htaccess

    deploy:
        cp -rv output/. /home/eeaol/public_html/

    redeploy: build deploy

I also scripted a command in `~/bin`, `reweb`, that runs `make redeploy` for
this project from anywhere on my machine, so that uploading new content to
[notes][] is as simple as

    webify newcontent 
    reweb

Which satisfies my need to do everything in the command line.

[notes]: http://homepages.see.leeds.ac.uk/~eeaol/notes/

The source code for this site is on [Github][].

[Github]: https://github.com/aaren/web

### Maths ###

Implemented with [MathJax][]. We're going to use [python-markdown-mathjax][].
Install it like this (assuming [python-markdown][] is already installed):

    md_ext_dir=$(python -c 'import markdown; print markdown.__path__[0]')
    cd ${md_ext_dir}/extensions
    wget https://github.com/mayoff/python-markdown-mathjax/blob/master/mdx_mathjax.py
    mv mdx_mathjax.py mathjax.py

[MathJax]: http://www.mathjax.org/
[python-markdown-mathjax]: https://github.com/mayoff/python-markdown-mathjax
[python-markdown]: http://pypi.python.org/pypi/Markdown/

Now in the template `page.html` we add to the header:

    ::html
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
                    "tex2jax": { inlineMath: [ [ '$', '$' ] ] }
                           });
    </script>

    <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML">
    </script>

Now in the markdown source, inline Latex is surrounded by `$ ... $` and for
equations we use `$$ .. $$`.

We then have to build poole with 

    poole --build --md-ext='codehilite(guess_lang=False)' --md-ext='mathjax()

Here's the [commit](https://github.com/aaren/web/commit/b9feafb).
