post: single user python imports
date: 2012-03-06
---

User install of Python modules
------------------------------

This came about because I wanted the [python-markdown][py-md] for
generating the content on this site using [Poole][] or [Chisel][].

[py-md]: http://freewisdom.org/projects/python-markdown/
[Poole]: https://bitbucket.org/obensonne/poole
[Chisel]: https://github.com/dz/chisel

On my university machine I don't have any admin rights, which is
almost certainly for the best. However, this means that I can't
install my own python modules in a standard way.

It is quite easy to install modules to my user account. For
modules with their own setup.py, just do

    python setup.py install --user

This is described in the [python documentation][user-doc] and it
installs to ~/.local.  Alternatively we can install to the 
[home directory][home-doc],

    python setup.py install --home=~

[user-doc]: http://docs.python.org/install/index.html#alternate-installation-the-user-scheme
[home-doc]: http://docs.python.org/install/index.html#alternate-installation-the-home-scheme

The user scheme is preferred as it is then immediately available
to import within python. If the home scheme is used, the PYTHONPATH
environmental variable needs to be set,

bash:

    export PYTHONPATH=$HOME/lib/python:$PYTHONPATH

csh:

    setenv PYTHONPATH $HOME/lib/python:$PYTHONPATH 

If the module uses easy_install,
    
    easy_install --prefix=$HOME/.local/ someeasyinstallablemodule

Or with pip,

    pip install --user somemodule
    

Summary
-------

Install the markdown python module without admin (root) rights like
this:

    cd ~/make
    wget http://pypi.python.org/packages/source/M/Markdown/Markdown-2.1.1.tar.gz#
    tar xvzf Markdown-2.1.1.tar.gz
    cd Markdown-2.1.1.tar.gz
    python setup.py install --user

    
