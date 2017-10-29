First you need ubuntu lamp distribution.

Additionally I've changed mysql with mariadb and install aptitude.

`aptitude install exim4-daemon-heavy exim4 mariadb-server clamav dovecot \`  
`dovecot-mysql dovecot-sieve dovecot-managesieved libapache2-mod-wsgi \`  
`libmariadb-client-lgpl-dev libmariadbd-dev libmariadb-client-lgpl-dev-compat \`  
`virtualenv clamav-daemon roundcube roundcube-plugins-extra roundcube-plugins \`  
`spamassassin php-zip`

MySQL-python needs mysql_config but is's missing even with libmariadb-client-lgpl-dev-compat! So:  
ln -s /usr/bin/mariadb_config /usr/bin/mysql_config

git clone https://github.com/ventricola/exim-dovecot-mysql-mailserver.git `<somewhare>`

a2enmod ssl  
a2enconf django-wsgi.conf  
a2enconf postmaster.conf  

Edit what necessary. At least replace fakedomain.tld everywhere  proper domain name.
Put everything in place. I use /var/www/html for mailctl.

Generate certs:  
openssl genrsa -out /etc/exim4/dkim.fakedomain.tld.key 2048  
openssl rsa -in /etc/exim4/dkim.fakedomain.tld.key -pubout -out /etc/exim4/dkim.fakedomain.tld.crt  

Add DNS records like:

`fakedomain.tld. IN TXT "v=spf1 mx a ip4:1.1.1.1/32 include:_spf.google.com ?all"`  
`dkim._domainkey.fakedomain.tld. IN TXT "k=rsa; p=MIIBIjA...DAQAB"`  
`_dmarc.fakedomain.tld.     899     IN      TXT     "v=DMARC1; p=none; sp=none; rua=mailto:postmaster@fakedomain.tld fo=1"`  

Cd to mailctl activate virtualenv or ever reinstall it first, then reinstall requirements.  
pip uninstall -r requirements.txt  
pip install -r requirements.txt  

