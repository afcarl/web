menu-position: 90
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

If we want to put posts into the notes section of the site and want
them to appear in the page we need to do a couple of things.

+ filename needs to be in the format `blog.yyyy-mm-dd.post_title.md`
+ The file needs to have `---` at the start.

I don't know why the second is the case, but that's what works.

This is something that is easily scripted. The idea is that I'll have
some notes written in Markdown somewhere on my machine and then do
`webify filename` and have it appear in the blog section of the website.

`Webify` looks something like this (in bash):

    #!bash
    filepath=$1
    # file may or may not have .extension
    filename=$(basename ${filepath})
    short_filename=${filename%.*}

    # where is the webpage input dir?
    input_dir=/home/eeaol/web/input/notes

    # get the date from the file, assuming dd/mm/yyyy format and
    # converting to yyyy-mm-dd
    date=$(grep '[0-9]./[0-9]./[0-9]...' $filename |\
            sed -e 's/^[^0-9]*//' \
                -e 's/\(..\)\/\(..\)\/\(....\)/\3-\2-\1/')


    newfilepath=${input_dir}/notes.${date}.${short_filename}.md
    cp $filepath $newfilepath 

    # add the --- to the start of the file
    echo "---" >> tmpf
    cat $newfilepath >> tmpf
    mv tmpf $newfilepath
    rm -f tmpf


Syntax Highlighting
-------------------

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

The source code for this site is on [Github][].

[Github]: https://github.com/aaren/web

Clean URLS
----------

This was a bit more hassle, but not that much. In the template page
there is some inline python which creates the menu automatically for
any page that contains "menu-position" metadata. We just need to change
this so that it points to clean urls.

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
