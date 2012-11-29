title: Putting maths in my blog
post: maths markdown
date: 2012-11-19
---

Here I'm going to try and make [MathJax][] work with my blog setup.

[MathJax]: http://www.mathjax.org/

We're going to use [python-markdown-mathjax][]. Install it like this
(assuming [python-markdown][] is already installed):

    md_ext_dir=$(python -c 'import markdown; print markdown.__path__[0]')
    cd ${md_ext_dir}/extensions
    wget https://github.com/mayoff/python-markdown-mathjax/blob/master/mdx_mathjax.py
    mv mdx_mathjax.py mathjax.py

[python-markdown-mathjax]: https://github.com/mayoff/python-markdown-mathjax
[python-markdown]: http://pypi.python.org/pypi/Markdown/

Now in the template `page.html` we add to the header:

    :::html
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
                    "tex2jax": { inlineMath: [['$', '$']] }
                           });
    </script>

    <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML">
    </script>

<s>and build poole with

    poole --build --md-ext='codehilite(guess_lang=False)' --md-ext='mathjax()
</s>

Now in the markdown source, inline Latex is surrounded by `$ ... $` and for
display math we use `$$ .. $$`.

Then we should find that $1 + 1 = 2$ right here and further that

$$ e^{i * \pi} + 1 = 0 $$

And, shockingly, that worked first time! Commit [here](https://github.com/aaren/web/commit/b9feafb)

We can also try \\( 2 + 2 = 5 \\) and

\\[ 1 = 0 \\]

which I marked up with `\\( ... \\)` and `\\[ .. \\]`. Any inline
math has to be defined explicitly, as in the html header above. So
I had to add an extra entry to the list: `[['$', '$'], ['\\(', '\\)']]`

We can label equations with a simple `label{}` and reference them
with a `\ref`, like in \ref{eq:beauty} below. See the 
[mathjax docs][mathjax-tex] for more. We need to add something to 
the header as well (MMLorHTML is to make it work in firefox):

[mathjax-tex]: http://docs.mathjax.org/en/latest/tex.html

    :::html
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
                    "tex2jax": { inlineMath: [['$', '$'], ['\\(', '\\)']] },
                    TeX: { equationNumbers: { autoNumber: "AMS" } },
                    MMLorHTML: { prefer: { Firefox: "HTML" } }
        });
    </script>

\begin{equation}
\label{eq:beauty}
e^{i * \pi} + 1 = 0 
\end{equation}

The problem with this is that it only works on MathJax *TeX*, not on
tex2jax. So equations marked up with `$$ .. $$` won't be numbered.

