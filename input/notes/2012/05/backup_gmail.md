Title: Backing up my gmail account
post: backup gmail
date: 2012-05-03
---

I got nervous that Google had the only copy of the last 10 years of
my email life. Enter [offlineimap][]

[offlineimap]: http://www.offlineimap.org

I use this for my work emails anyway, I just needed to tweak it a
bit and do these things:

* Download the latest offlineimap (mine was an old 5.9 version for
  some reason that I can't remember)

* Create a special offlineimaprc especially for gmail

* Create a folder for the backup maildir to go into
    
Download the source and link it up:

    cd ~/make
    git clone https://github.com/spaetz/offlineimap.git
    cd ~/bin
    ln -s ~/make/offlineimap/offlineimap.py offlineimap

Make a file called 'gmail_imaprc', containing the following:

    [general]
    accounts = Gmail
    maxsyncaccounts = 3

    [Account Gmail]
    localrepository = Local
    remoterepository = Remote

    [Repository Local]
    type = Maildir
    localfolders = /home/eeaol/private/gmail

    [Repository Remote]
    type = IMAP
    remotehost = imap.gmail.com
    remoteuser = USERNAME@gmail.com
    remotepass = PASSWORD
    ssl = yes
    maxconnections = 1
    realdelete = no

Make a folder called 'gmail' in a place where there is enough room
for all of the emails (~2GB for me). I used a symlink to a big disk.

Then just run (-u blinkenlights is for pretty colours)

    offlineimap -c gmail_imaprc -u blinkenlights

Three hours later, Gmail is backed up. Panic over.

### See also  ###

[h4ck3r](http://www.h4ck3r.net/2011/03/13/gmail-backup-imap/)

[Enigma Curry](http://www.enigmacurry.com/2008/02/22/backing-up-my-online-brain/)

[Mutt / Gmail / Offlineimap](http://pbrisbin.com/posts/mutt_gmail_offlineimap)

[More generally](http://pbrisbin.com/posts/two_accounts_in_mutt)
