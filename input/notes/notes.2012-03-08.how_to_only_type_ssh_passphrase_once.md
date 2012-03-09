---
Date: 08/03/2012

Using ssh to shell into remote machines is useful. If you do it 
a lot, typing in the password everytime becomes a bit annoying.
Plus, any scripts that login to remote machines will need the 
password to be supplied to them.

The solution is to add your public key to the list of authorised
keys on the remote machine. Put the contents of ~/.ssh/id_rsa.pub
(on your machine) into ~/.ssh/authorized_keys (on the remote machine).

You can now do ssh remotemachine and not have to enter a password.
However, this isn't especially secure. It means that anyone that
manages to access your keys has access to any of the machines you've
added your public key to. This is very not good.

The solution here is to use a ssh passphrase. Regenerate your ssh keys
with

    ssh-keygen -p

and accept the default locations by hitting return. Enter a passphrase
when prompted. Make it really long. If you already have a passphrase,
this command will let you change it without changing the keys.

Great. Now we're back where we started, having to enter a really long
passphrase every time we want to ssh. This is where ssh-agent comes in.
In a single shell session,

    :::bash
    eval $(ssh-agent)
    ssh-add

would make you enter your passphrase and then remember it for the rest of
that session. But what about working across multiple sessions?

At work I use both bash and csh on kde. We need to tell bash and csh to 
look for the ssh-agent in a specific place. In bash,

    :::bash
    export SSH_AUTH_SOCK=/tmp/$USER.agent

in csh,

    :::csh
    set SSH_AUTH_SOCK=/tmp/$USER.agent

Then we need to get a single instance of ssh-agent running on login that
will remember the passphrase for all of my shell sessions. In KDE, that
means autostarting something, so in ~/.kde/Autostart, make a file
called ssh-agent (name doesn't matter) that reads

    #!/bin/bash
    ssh-agent -a /tmp/$USER.agent
    ssh-add

Now on all subsequent logins we will be prompted for our passphrase
on login and never again!

I use Openbox instead of KDE at home. Autostarting in Openbox is done
by creating a file ~/.config/openbox/autostart containing any commands
you want to run on startup, i.e. including the above.

If you don't use csh or bash or KDE or Openbox, I can't help you.
