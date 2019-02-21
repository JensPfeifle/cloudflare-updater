Cloudflare DNS Updater
=====================

Update cloudflare AAAA record via the API because ddclient is unfriendly towards IPv6.

Requires python3 and the requests module.

cron entry: 
------------
```17 * * * * /usr/bin/python3 /opt/dnsupdate.py```
