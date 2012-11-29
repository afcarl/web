title: Interactive comments in web pages
post: inline comments and highlighting
date: 2012-11-23
---

I want to allow people to post comments on things that I write, but
for those comments to be linked to the content that they are
referencing, rather than sitting in a block at the end of the
article.

This isn't particularly widespread, but I found a few
implementations.

- [highlighter][] allows highlighting of content in a page, and
  commenting specifically on that.
- [iscribbled][] allows comments that are attached to specific `<div>
  .. </div>` elements of your page.

Highlighter only took a trivial change to get going, adding a code
snippet to the bottom of the body of my template page. *This is
specific to my site!*

    ::html
    <script type='text/javascript'>
        var _hl=_hl||{};
        _hl.site='2890';
        (function(){
            var hl=document.createElement('script');
            hl.type='text/javascript';
            hl.async=true;
            hl.src=document.location.protocol+'//highlighter.com/webscript/v1/js/highlighter.js';
            var s=document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(hl,s);
                })();
    </script>

[highlighter]: http://highlighter.com
[iscribbled]: http://www.iscribbled.com/

I've only enabled it on this page for now.

<script type='text/javascript'>
    var _hl=_hl||{};
    _hl.site='2890';
    (function(){
        var hl=document.createElement('script');
        hl.type='text/javascript';
        hl.async=true;
        hl.src=document.location.protocol+'//highlighter.com/webscript/v1/js/highlighter.js';
        var s=document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(hl,s);
            })();
</script>
