title: Setting up Enthought in a VirtualEnv
post: virtualenv with enthought
date: 2012-04-02
---

In my work environment, there are a load of pre compiled applications
available to me just by `app setup gifmerge` or similar. One app that
I use all the time is [Enthought][], a comprehensive scientific tool
suite for Python. The system python is 2.4, but by adding

    app setup enthought

to my .bash/cshrc I get python 2.7.2 and loads of useful modules (e.g.
[numpy][], [matplotlib][]) and programs (e.g. [pygments][], [flake8][])
available to me in all my shells.

[Enthought]: www.enthought.com
[numpy]: http://numpy.scipy.org/
[matplotlib]: http://matplotlib.sourceforge.net/
[pygments]: http://pygments.org/
[flake8]: http://pypi.python.org/pypi/flake8

At home I use Debian Squeeze. The python version is 2.6. If I want the
latest python I could just download the python [source][python2.7.2]
and

    ./configure
    make
    make altinstall

to have it available to me by running `python2.7` and avoiding breaking
the system python (n.b. make *altinstall*).

[python2.7.2]: http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz

But what if I want all of Enthought? And I want to be able to switch it on 
and off so that I can go back to a clean Squeeze environment if I want to? 
The solution involves [virtualenv][ve] and some useful extensions provided 
by [virtualenvwrapper][vew]

[ve]: http://pypi.python.org/pypi/virtualenv/
[vew]: http://pypi.python.org/pypi/virtualenvwrapper/

To install virtualenvwrapper,

    pip install virtualenvwrapper

To get virtualenvwrapper going we need to add some bits to .bashrc, thanks
to [this site][jontourage].

    WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh

[jontourage]: http://jontourage.com/2011/02/09/virtualenv-pip-basics/

Install Enthought, which is free using the [free][free-epd] version of 
Enthought, or [with an academic license][academic-epd]. I did this with
EPD-7.3-2-rh5-x86.

[free-epd]: http://www.enthought.com/products/epd_free.php
[academic-epd]: http://www.enthought.com/products/edudownload.php

Now we can follow the method [here][decomposition] to have Enthought working
with virtualenv.

[decomposition]: http://seanjtaylor.com/2011/03/03/getting-epd-to-play-nicely-with-virtual-environments/

    export EPD="$HOME/src/epd"
    cd $EPD
    bin/easy_install virtualenv
    bin/virtualenv $WORKON_HOME/epd

Then change a section of `$WORKON_HOME/epd/bin/activate` from

    VIRTUAL_ENV="$HOME/.virtualenvs/epd"
    export VIRTUAL_ENV

    _OLD_VIRTUAL_PATH="$PATH"
    PATH=$VIRTUAL_ENV/bin:$PATH
    export PATH

to

    EPD="$HOME/src/epd"
    VIRTUAL_ENV="$HOME/.virtualenvs/epd"
    export VIRTUAL_ENV

    _OLD_VIRTUAL_PATH="$PATH"
    PATH="$EPD/bin:$VIRTUAL_ENV/bin:$PATH"
    export PATH 

Then we create the virtualenv for epd:

    mkvirtualenv --distribute epd

You'll want to get pip installing and upgrading packages in
Enthought as well, which means we can't use the pip that comes in
the virtualenv.

    cd $EPD
    easy_install pip

And we can now get enthought as a working environment by

    workon epd
    ...do some work...
    ...finished...
    deactivate
