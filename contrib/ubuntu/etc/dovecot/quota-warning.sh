#!/bin/sh
PERCENT=$1
USER=$2
cat << EOF | /usr/lib/dovecot/dovecot-lda -d $USER -o "plugin/quota=maildir:User quota:noenforcing"
From: postmaster@fakedomain.tld
Subject: quota warning

Your mailbox is now $PERCENT% full.
EOF