title: Highlighting sub regions of python code
post: vim python sub highlighting
date: 2012-10-23
---

Normally when writing in Vim with Markdown or RestructuredText,
indented blocks of code are highlighted in a single colour which I
find looks naff and unreadable. I would really like this code to
have syntax highlighting.

Vim has the capacity to highlight specific regions of the text in a
format different to that of the rest of the text.

In a simple file

    :syn include @py syntax/python.vim
    :syn region pythoncode start=/\.. python::/ end=/^$\n^$/ contains=@py

This catches explicit python directives like you would have in rst,
provided that they end with *two* blank lines.

I can't get this to apply in a file that already has it's own syntax
highlighting applied. To do this, you first need to do

    let b:current_syntax=''
    unlet b:current_syntax

Here's something that should work:

    function! Hi_Py ()
        " highlights python code in current rst document
        let b:current_syntax=''
        unlet b:current_syntax
        syntax include @py syntax/python.vim
        syntax region pythoncode start=/\.. python::/ end=/^$\n^$/ contains=@py
    endfunction
    
    map <leader>h :call Hi_Py ()<CR>

What I'd really like to do is have the directive at the start of the
block be used to set the syntax highlighter for that block, so that
we aren't limited to python. I rarely use non python though so this
isn't a priority for me.

[Here][vim-wiki] is the vim wiki page on the subject.

[vim-wiki]: http://vim.wikia.com/wiki/Different_syntax_highlighting_within_regions_of_a_file

Related is [this][sagerst] method for highlighting markup in python docstrings.

[sagerst]: http://thales.math.uqam.ca/~labbes/blogue/2011/06/rest-syntax-highlighting-for-sage-docstrings-in-vim/
