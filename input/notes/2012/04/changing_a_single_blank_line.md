title: Changing a single blank line in a file
post: changing a single blank line
date: 2012-04-16
---

Well this has turned out to be a lot more convoluted than I expected.

Here's the situation: there is a file that consists of a header and some
content. The header contains no blank lines and is separated from the content
by one blank line. The content might contain any number of blank lines.

What I want to do is change the separation between the header and content from
a single blank line to a blank line followed by a string ('---' in this case).

Return the header and the blank line:

    sed '/^$/q' file

return just the header:
    
    sed '/^$/Q' file

return the content:

    sed '1,/^$/d' file


To concatenate the output from these together and put a '---' and a blank line
inbetween and put this into a newfile, all in a single line:

    sed '/^$/Q' file && echo -e "---\n" && sed '1,/^$/d' file > newfile
