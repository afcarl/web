title: How to make movies from images
post: creating movies from images
date: 2012-04-17
---

Let's say that there's a directory with a load of images in it with 
some logical, ordered naming convention (assuming something like
img_somenumbers.image_extension). We want to animate these images.

One way (if the images are .gif) is to use `gifmerge` to make an
animated gif, e.g. for 0.5s frame delay and looping forever:

    gifmerge -50 -l0 img*.gif > animation.gif

We could use ImageMagick:

    convert -delay 50 img*.gif animation.mpg

Or if without making a file:

    animate img*.gif

These are all simple commands and might be fine for simple problems.
ImageMagick will allow converting between lots of image types, resizing,
adding text and lots more. However, for fine control over the animation
quality it might be easier to use [ffmpeg][] (this is all that ImageMagick
is doing anyway).

The requirement of using ffmpeg is that the source files are numbered
sequentially (e.g. img0001.png, img0002.png...). Then we can do
something like (thanks to [Werner][] for the tip),

    ffmpeg -qscale 5 -r 4 -b 9600 -s sxga -i img%04d.png animation.mp4

* qscale 5: A quality setting between 1 and 31. 1 is best. 
* r 4: 4 frames per second
* b 9600: bitrate in b/s (default is 200)
* s sxga: sxga means 1280x1024. Can specify arbitrart wxh or things like
        hd1080, vga, or nothing at all to use the input size.
* i img%04d.png: the sequential number consists of 4 numbers at this
                position in the filenames
* animation.mp4: output file. Can experiment with different extensions,
                e.g. .flv, .mpg


[ffmpeg][] is much faster than convert and also allows you a lot more
control.

If your files aren't numbered sequentially but they are in the order you
want with `ls`, here's a bash script that will copy and renumber them for
you:

    #!/bin/bash
    indir=$1
    outdir=$2
    ext=$3
    i=0
    for f in $(ls ${indir}/*${ext}); do
        newf=$(printf "%04d.%s" ${i} ${ext})
        cp -v $f ${outdir}/${newf}
        let i=i+1
    done

Let's say you call it `numerate`, then e.g.

    numerate images numbered .png

will take *.png from 'images', renumber them and put them in 'numbered',
which is a directory that you hopefully created for the purpose. Then
just go into 'numbered' and do the ffmpeg stuff in there.


[ffmpeg]: http://ffmpeg.mplayerhq.hu/
[Werner]: http://www.miscdebris.net/blog/2008/04/28/create-a-movie-file-from-single-image-files-png-jpegs/
[mit]: http://electron.mit.edu/~gsteele/ffmpeg/
[utpp]: https://developers.google.com/youtube/player_parameters
