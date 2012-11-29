title: make GNU Screen and Vim play nice in 256 colours
post: vim screen
date: 2012-04-15
---

#### Update ####

To get vertical split and 256 colors working in screen, just use
the [git version][git-screen] of screen.

[git-screen]: http://git.savannah.gnu.org/cgit/screen.git/

    cd ~/make
    git clone git://git.sv.gnu.org/screen.git
    cd screen/src
    ./autogen.sh
    ./configure --prefix=$HOME/.local --enable-colors256
    make
    make install

In ~/.screenrc (this is the only thing you need):
   
    # redraw the background colour
    defbce "on"

#### Original ####

Making vim work with 256 colours in a screen session can be a bit
of a hassle. The 'solution' is below.

Vertical split patch and 256 colors:

    cd ~/make
    wget http://ftp.gnu.org/gnu/screen/screen-4.0.3.tar.gz
    tar xvzf screen-4.0.3.tar.gz
    wget http://vsp4sdl.yuggoth.org/wrp_vertical_split_0.3_4.0.2.diff.bz2
    bunzip2 -v wrp_vertical_split_0.3_4.0.2.diff.bz2
    cd screen-4.0.3
    patch -p1 < ../wrp_vertical_split_0.3_4.0.2.diff 
    ./configure --enable-colors256
    make
    make install

http://stackoverflow.com/questions/1630013/vim-colorschemes-in-screen-putty

256 colours in ~/.screenrc:

    # terminfo and termcap for nice 256 color terminal
    # allow bold colors - necessary for some reason
    attrcolor b ".I" 
    # tell screen how to set colors. AB = background, AF=foreground 
    termcapinfo xterm 'Co#256:AB=\E[48;5;%dm:AF=\E[38;5;%dm' 
    # erase background with current bg color 
    defbce "on"
