
post: git stash
date: 2012-03-07
---

I have three branches for one of my labwork coding projects: a stable,
always working master branch, a dev branch in which I fix things continually
and branch out from to feature branches in which I add new functionality.

Anyway, I accidentally made some changes in master when I thought I was 
working in dev. I haven't commited or added new files. The solution is to
use git stash.

I made a new file in these changes, and this has to be added before stashing.

    git add .
    git stash
    git checkout dev
    git stash pop

If I had made a commit, I could first go back one commit whilst maintaining
my changes in the index and working tree:

    git reset --soft HEAD^
