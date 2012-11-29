title: Installing tmux on CentOS 5
post: installing tmux
date: 2012-11-15
---

I got tired of GNU Screen. I find it fine for simple use, but changing even the
simplest thing, like the colour of things on the screen, is an unintuitive
hassle. I'd looked at [tmux][] before but never bothered to give it a go.
Obviously, it wasn't available on my system and it wouldn't compile for me
straight away.

This is on CentOS 5 with no root access.

First I needed to get [libevent][] which was the one dependency
that tmux complained about.

[libevent]: https://github.com/libevent/libevent

Installing this required a trick. When trying to use `autogen.sh` I got an
error to do with autoconf, m4_pattern_allow and AC_PROG_SED. Having no idea
what any of this means I added a line to `configure.ac`:

    ::git
    diff --git a/configure.ac b/configure.ac
    index 3f91ce0..473732e 100644
    --- a/configure.ac
    +++ b/configure.ac
    @@ -44,6 +44,7 @@ dnl the 'host' machine is where the resulting stuff runs.

    dnl Checks for programs.
    AM_PROG_CC_C_O
    +m4_pattern_allow([AC_PROG_SED])
    AC_PROG_SED
    AC_PROG_INSTALL
    AC_PROG_LN_S

Then I could run `autogen.sh` and install as normal (`--prefix=$HOME/.local`).

To install tmux I needed to tell it to use the library I'd just made for
it:

    ./configure CPPFLAGS=" -I$HOME/.local/include" LDFLAGS=" -L$HOME/.local/lib" --prefix=$HOME/.local
    make
    make install

and added a line to my bashrc:

    ::bash
    export LD_LIBRARY_PATH=$HOME/lib/:$LD_LIBRARY_PATH

Tmux now starts up, at least!

Not feeling like I'd procrastinated enough, I continued on this tedious
rampage by installing [mocp][], which had previously resisted attempts
due to not being able to find any decoder libraries.

[mocp]: http://moc.daper.net/
