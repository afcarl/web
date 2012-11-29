title: Mocp installation
post: installing mocp
date: 2012-11-16
---

[Mocp][] is a great ncurses music player that has a nice interface and plays
in the background. When you close the client, the music keeps on playing
leaving less clutter around your desktop.

[Mocp]: http://moc.daper.net/

I'm using a CentOS 5 workstation that I do not have root access to and 
which only had mplayer as another working media player. Mplayer doesn't
have an interface, which was a bit tiresome. 

Mocp needed libraries in order to play anything. Obviously I didn't just
stop at mp3 support (libmad), but added in flac, theora, resampling and
other goodies. This isn't actually very difficult, you just need to know
the right incantations.

Libraries installed:
- libmad-0.15.1b
- libid3tag-0.15.1b
- libtheora-1.1.1
- flac-1.2.1
- libogg-1.3.0
- libvorbis-1.3.3
- libsndfile-1.0.25
- libsamplerate-0.1.8

for all of the above, download, extract and change to the directory, then

    ./configure --prefix=$HOME/.local
    make
    make install

Add these to bashrc as well, or you won't pick up sample rate, flac and others.
The LD_LIBRARY thing is so that programs that you run know to look for local
libraries as well. This is useful for other locally installed, library
dependent programs as well, like [tmux]

    export PKG_CONFIG_PATH=$HOME/.local/lib/pkgconfig
    export LD_LIBRARY_PATH=$HOME/.local/lib/:$LD_LIBRARY_PATH

Finally we can install moc. Download, extract, cd, then

    ./configure CPPFLAGS=" -I$HOME/.local/include" LDFLAGS=" -L$HOME/.local/lib" --prefix=$HOME/.local
    make
    make install
    mocp

Enjoy!
