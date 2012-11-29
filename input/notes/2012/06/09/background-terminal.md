title: How to setup a background terminal in crunchbang / openbox
post: background terminal
date: 2012-06-09
---

I tried a couple of times to setup a background terminal in Crunchbang
by [faffing around with Terminator][cb-terminator]. I never managed to
get it to work satisfactorily though, probably because the linked howtos
were based on older versions of Crunchbang.

The [Arch wiki][arch-tilda] suggests using Tilda, a fullscreen terminal
like what you get in Quake or Half-Life. This was much easier.

[cb-terminator]: http://crunchbanglinux.org/wiki/howto_have_terminator_become_your_wallpaper
[arch-tilda]: https://wiki.archlinux.org/index.php/Terminal_as_a_Transparent_Wallpaper

Install Tilda somehow, `sudo apt-get tilda`.

Now either start it and right-click to edit the preferences, or directly
edit `~/.tilda/config_0` to set the geometry how you want it. Make sure
to enable transparency if you want to see your wallpaper behind.

Now edit `~/.config/openbox/rc.xml` and in the "applications" section
add

    <application name="tilda">
    <layer>below</layer>
    </application>

We'll want it to start automatically, so put `tilda &` somewhere in
`~/.config/openbox/autostart.sh`.

Restart and it works great. The only issue with Tilda is that it
doesn't have some of the more advanced features that Terminator has like
window splitting. But for the reasons I want a background terminal, i.e.
quick jobs, this isn't an issue.

If you're running Conky and find it has disappeared, just decrease the
width of Tilda so that it stops covering it.

