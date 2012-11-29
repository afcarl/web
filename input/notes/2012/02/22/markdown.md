title: Markdown
post: markdown
date: 2012-02-22
---

I really like plain text. I really don't like using office programs if
I can avoid it. The ability to open up a document, for which the intent
is to communicate written language, in Vim and to use sed / grep on that
document is very useful and very important to me.

There are lots of ways to format documents written in plain text. You can
entirely make up your own formatting for emphasis, headings and references
but it would be nice to be consistent between different authors. Furthermore,
whilst well formatted plain text is quite readable it can be made more
readable by use of italics, bold, superscripts, underlining and variable text
size.

I came across Markdown recently. Markdown is essentially a highly readable
programming language which can be run through a compiler to produce a
formatted document. But this formatting is preserved in the source - a
file written in markdown is still entirely legible and comprehensible when
read through a simple text editor.

Paragraphs in Markdown are one or more consecutive lines of text, separated
by one or more blank lines. This means that text can be written with a
constant character width and not have long lines that need wrapping to read.

Headers in Markdown can be written
==================================
equally, 
=
# or,
# equally, #

Sub-headers
-----------
## also ## 

Quoting
=======
As in email, markdown uses > for quoting.

> For example, we can put a >
> before every line

> equally, we can be lazy and just put one before
the paragraph, but this is less readable.

> quotes can,
> > of course,
> > > be nested.

# Lists #
+ can
+ be
+ unordered
1. or
2. have numbers in the source
3. but it doesn't matter - the output is the same line order as written.
   Hanging indents are good, but not mandatory.

100\. The previous number is besides the point, but accidental list creation
can be avoided by escaping the period with a \.

Code Blocks
===========
Code can be inserted into a Markdown document by

    print "Indenting the lines of a block"

Horizontal Rules
***
Are easy and just require three or more -, * or _ on a line by themselves.
_ _ _

Links
=====

1. Inline
   ------
   This is [the link text](http://www.b3ta.com, "optional title text")
   an inline link.

2. Reference
   ---------
   This is [how a reference link works] [id], by using an id that can be
   expanded anywhere in the document.

   [id]: http://www.kernel.org "optional title text"

   The id is *not* case sensitive. Further an [implicit][] id can be made.

   [implicit]: http://www.guardian.co.uk

Emphasis
========
* and _ are used as indicators of emphasis. Single <em>, double <strong>.

Again, literals are produced using \ to escape.

Inline Code
===========
Here is some example Python: `Image.open('spam').rotate(45)`

Images
======
Obviously, images can't be displayed in a plain text file. Rather, they are
indicated by links prefixed by a !.


Source
======
These notes were written whilst reading through the guide to Markdown
syntax at [Daring Fireball].

[Daring Fireball]: http://daringfireball.net/projects/markdown/syntax
