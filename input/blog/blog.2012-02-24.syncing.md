---
Date: 24/02/2012

Synchronising multiple work spaces
----------------------------------
I have two main workspaces: my university account and my laptop, both
linux environments (CentOS 5.1 and Debian Squeeze). Files stored on my
university account are backed up on a daily basis and I have access to
a number of fast machines for data processing - this makes working on
my uni account, either locally in my office or remotely through ssh,
the preferred way of doing things.

However, I am frequently in a situation where I don't have network
access, e.g. field work, travelling, low battery on my laptop. I often
write a lot / download and read a lot of papers in these situations
(probably exactly because I can't get on a network) and end up with
a lot of stuff I need to copy back into my uni account.

There are two distinct cases here:

    1. Distinct new files (e.g. pdfs)
    2. Modified codebase / writing.

I use git for version control, which I'll come to later. First I'll
deal with synchronising files using **rsync**.

### Rsync ###

Local folder to remote folder:

    rsync -r -a -v -e "ssh -l eeaol" --delete ~/testy/ my-ssh-gw.ac.uk:~/test2

sender: ~/testy
destination: eeaol@see-gw-01.leeds.ac.uk:~/test2

-r : recursive
-a : archive mode (preserves file modification times and more).
-v : verbose
-e "ssh -l eeaol" : use ssh with user eeaol
--delete: potentially dangerous. deletes files on the destination side
          not present on the send side.

As a first guess this does something right, but I have to be very careful not
to delete new files that I want.

What I typically have is a folder on each machine full of papers
(as pdf) that have an identical bulk of papers, but some new ones in
both of the directories. To deal with this I have to use rsync twice,
once in both directions:

    rsync -auzrv -e ssh ~/home/path eeaol@my-ssh-gw.ac.uk:~/office/path
    rsync -auzrv -e ssh eeaol@my-ssh-gw.ac.uk:~/office/path ~/home/path

-r : recursive
-a : archive mode (preserves file modification times and more).
-v : verbose
-e ssh : use ssh
-z : use compression
-u : skip files that are newer on the destination 

But the problem with this is that it copies all of the files over even
when the two directories are identical!

TODO: more content here


### Git ###

I have accounts with github.com and bitbucket.org. I use github for
coding projects that I use in my research and private repositories on
bitbucket for my notes and more experimental coding.

The new user guide at Github is excellent, whereas BitBucket seems to
assume some prior knowledge. One problem that I had was that ssh would
not work from my local (office) machine. A workaround for this is to
use a proxy; in `~/.ssh/config` put

    Host github.com
    ProxyCommand /usr/local/bin/corkscrew see-gw-01.leeds.ac.uk 8000 %h %p
    Host bitbucket.org
    ProxyCommand /usr/local/bin/corkscrew see-gw-01.leeds.ac.uk 8000 %h %p

and ssh works for these sites. ssh can be tested by

    ssh git@github.com
    ssh git@bitbucket.org

which both return something along the lines of shell access not allowed.

### Usage ###

If I'm working on a git managed project in a local repo and I want to
push the changes to one of my web repos, I need to first define where
to push to
    
    git remote add github git@github.com:aaren/projectname.git

and create a new repo called projectname on GitHub. Then I just do
    
    git push -u github master

and the master branch is pushed to GitHub. If I also wanted to have
this project mirrored on BitBucket I can do

    git remote add bitbucket git@bitbucket.org:aaaren/projectname.git
    git push -u bitbucket master


If I want to work on my own source code on another machine I do

    git clone git@github.com:aaren/projectname.git

If I want to clone someone elses repo, for example Steve Losh's `t`,

    git clone http://github.com/sjl/t.git


