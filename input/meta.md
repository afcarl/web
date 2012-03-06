menu-position: 99
date: 06/03/2012
---
06/03/2012

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
    input_dir=/home/eeaol/web/input/blog

    # get the date from the file, assuming dd/mm/yyyy format and
    # converting to yyyy-mm-dd
    date=$(grep '[0-9]./[0-9]./[0-9]...' $filename |\
            sed -e 's/^[^0-9]*//' \
                -e 's/\(..\)\/\(..\)\/\(....\)/\3-\2-\1/')


    newfilepath=${input_dir}/blog.${date}.${short_filename}.md
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

