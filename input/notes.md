
menu-position: 10
---
Sometimes I write words about things.

<!--%
from datetime import datetime
posts = [p for p in pages if "post" in p] # get all blog post pages
posts.sort(key=lambda p: p.get("date"), reverse=True) # sort post pages by date
for p in posts:
    date = datetime.strptime(p.date, "%Y-%m-%d").strftime("%B %d, %Y")
    clean_url = p.url.split('.html')[0] + '/'
    print "  * **[%s](%s)** - %s" % (p.post, clean_url, date) # markdown list item
%-->

