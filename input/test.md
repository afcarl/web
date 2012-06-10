title: test embeds
---

Hi, here are some tests:

### Simple embed of a swf: ###

Can be annoying for people as it plays automatically.

    <p><embed src="http://homepages.see.leeds.ac.uk/~eeaol/test.swf" height="600" width="800"/></p>

    <p><embed src="http://homepages.see.leeds.ac.uk/~eeaol/test.swf" height="600" width="800"/></p>

### Multiple levels of fallback: ###

Html5 -> local flash player -> direct download

Best option for local hosting.

See [video for everybody][vfe] for details. Requires adding two lines to
.htaccess:

    #!Apache
    AddType video/ogg .ogv
    AddType video/mp4 .mp4

[vfe]: http://camendesign.com/code/video_for_everybody

<!-- first try HTML5 playback: if serving as XML, expand `controls` to `controls="controls"` and autoplay likewise -->
<!-- warning: playback does not work on iOS3 if you include the poster attribute! fixed in iOS4.0 -->
<video width="800" height="640" controls>
    <!-- MP4 must be first for iPad! -->
    <source src="http://homepages.see.leeds.ac.uk/~eeaol/test.mp4" type="video/mp4" /><!-- Safari / iOS video    -->
    <source src="http://homepages.see.leeds.ac.uk/~eeaol/test.ogv" type="video/ogg" /><!-- Firefox / Opera / Chrome10 -->
    <!-- fallback to Flash: -->
    <object width="640" height="360" type="application/x-shockwave-flash" data="player.swf">
        <!-- Firefox uses the `data` attribute above, IE/Safari uses the param below -->
        <param name="movie" value="player.swf" />
        <param name="flashvars" value="controlbar=over&amp;image=test.jpg&amp;file=http://homepages.see.leeds.ac.uk/~eeaol/test.mp4" />
        <!-- fallback image. note the title field below, put the title of the video there -->
        <img src="test.jpg" width="640" height="360" alt="testing video"
             title="No video playback capabilities, please download the video below" />
    </object>
</video>
<!-- you *must* offer a download link as they may be able to play the file locally. customise this bit all you want -->
<p> <strong>Download Video:</strong>
    Closed Format:  <a href="http://homepages.see.leeds.ac.uk/~eeaol/test.mp4">"MP4"</a>
    Open Format:    <a href="http://homepages.see.leeds.ac.uk/~eeaol/test.ogv">"Ogg"</a>
</p>

### Forced local player: ###

Same as above, but forcing the use of the local player. Doesn't seem to be
woking as it is.

<object width="640" height="360" type="application/x-shockwave-flash" data="player.swf">
    <!-- Firefox uses the `data` attribute above, IE/Safari uses the param below -->
    <param name="movie" value="player.swf" />
    <param name="flashvars" value="controlbar=over&amp;image=test.jpg&amp;file=http://homepages.see.leeds.ac.uk/~eeaol/test.mp4" />
    <!-- fallback image. note the title field below, put the title of the video there -->
    <img src="test.jpg" width="640" height="360" alt="testing video"
            title="No video playback capabilities, please download the video below" />
</object>

    <object width="640" height="360" type="application/x-shockwave-flash" data="player.swf">
        <!-- Firefox uses the `data` attribute above, IE/Safari uses the param below -->
        <param name="movie" value="player.swf" />
        <param name="flashvars" value="controlbar=over&amp;image=test.jpg&amp;file=http://homepages.see.leeds.ac.uk/~eeaol/test.mp4" />
        <!-- fallback image. note the title field below, put the title of the video there -->
        <img src="test.jpg" width="640" height="360" alt="testing video"
                title="No video playback capabilities, please download the video below" />
    </object>

### Embedded Youtube:  ###

The easiest option, but data is hosted on youtube.

See [https://developers.google.com/youtube/player_parameters](https://developers.google.com/youtube/player_parameters)


<p><iframe type="text/html" width="640" height="390"
  src="http://www.youtube.com/embed/bSZsYTHriI8?autohide=1&rel=0"
  frameborder="0"></iframe></p>

    <p><iframe type="text/html" width="640" height="390"
    src="http://www.youtube.com/embed/bSZsYTHriI8?autohide=1&rel=0"
    frameborder="0"></iframe></p>
