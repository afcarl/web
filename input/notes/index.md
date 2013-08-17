title: notes
menu-position: 10
---
Sometimes I write words about things.

<!--%
from datetime import datetime
import re

posts = [p for p in pages if "post" in p] # get all blog post pages
posts.sort(key=lambda p: p.get("date"), reverse=True) # sort post pages by date
for p in posts:
    # strip out duplicates
    if not re.search(r'\/\d{4}\/\d{2}\/\d{2}\/', p.fname):
        date = datetime.strptime(p.date, "%Y-%m-%d").strftime("%B %d, %Y")
        clean_url = p.url.split('.html')[0]
        print "  * **[%s](%s)** - %s" % (p.title, clean_url, date) # markdown list item
%-->

