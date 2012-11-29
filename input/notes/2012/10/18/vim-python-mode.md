title: A very boring note: setting up python-mode in Vim
post: vim python mode
date: 2012-10-18
---

*Warning!: this post is very boring.*

I wanted to use [python-mode](https://github.com/klen/python-mode)
in Vim.

#### TL;DR ####

If you're having problems compiling vim to use a specific python
version: 

    make distclean
    ./configure --with-features=big --prefix=$HOME --enable-pythoninterp \
                --with-python-config-dir=/path/to/python/lib/python2.7/config

At the start of vimrc:

    let $PYTHONHOME='/path/to/python'

#### Problem ####

Starting vim after adding python-mode spat out an error, the essence
of which is

    :::python
    ImportError: cannot import name urandom

after which vim would start.

[Here](https://github.com/klen/python-mode/issues/87) is the issue
on Github. I don't have root / superuser access.

I got the same maddening bug on a centos system that I don't have
root / superuser access to.

[This](http://permalink.gmane.org/gmane.editors.vim.devel/34176)
gave me some clues as to the problem. I used Enthought 7.3-1, with
python version 2.7.3 (system default is 2.4). In vim `:py import
sys; print sys.version` gave 2.7.2.

The problem arises because the way to import urandom was changed
between 2.7.2 and 2.7.3 (as a security fix).

#### Solution ####

I 'solved' the problem by setting up Enthought 7.2-1 (with python 2.7.2), and
compiling vim 7.3 (system default is 7.0) with

    ./configure --with-features=big --prefix=$HOME --enable-pythoninterp \
                --with-python-config-dir=/apps/enthought-7.2-1/lib/python2.7/config

and at the top of `.vimrc`

    :::vim 
    let $PYTHONHOME='/apps/enthought-7.2-1/'

#### Caveat ####

I say 'solved' because I could not find a way to get vim to use python 2.7.3.
If I changed the config-dir above to 7.3-1, I get the following on
configuration:

    checking for python... (cached) /apps/enthought-7.2-1/bin/python
    checking Python version... (cached) 2.7
    checking Python is 1.4 or better... yep
    checking Python's install prefix... (cached) /apps/enthought-7.2-1
    checking Python's execution prefix... (cached) /apps/enthought-7.2-1
    (cached) checking Python's configuration directory... (cached) /apps/enthought-7.3-1/lib/python2.7/config

whereas with 7.2-1

    checking for python... (cached) /apps/enthought-7.2-1/bin/python
    checking Python version... (cached) 2.7
    checking Python is 1.4 or better... yep
    checking Python's install prefix... (cached) /apps/enthought-7.2-1
    checking Python's execution prefix... (cached) /apps/enthought-7.2-1
    (cached) checking Python's configuration directory... (cached) /apps/enthought-7.2-1/lib/python2.7/config

Then I gave up. It works with python 2.7.2. Python-mode is excellent, by the
way.

### Update ###

1/11/2012: I was forced to go further when enthought-7.2-1 was removed from the
system. The configure script is just a link to another configure in `src`,
which refers to a cache file `src/auto/config.cache` in which a load of
variables are preset.  This contained numerous references to enthought 7.2-1
and it persists after `make clean`. I renamed the file to `old.config.cache`
and compiled vim again. Now it works using the path to the enthought 7.3-1.

`make clean` doesn't remove the output from configure. The way to do
this is to run `make distclean`.
