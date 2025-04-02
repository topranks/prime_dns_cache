## Prime DNS Cache

This is a simple script I run to attempt to keep my DNS recursive resolve cache
warm, given there are not many users behind it.

#### Dependencies

It is a Python3 script that relies on dnspython and BeautifulSoup, to 
install on debian you can:
```
sudo apt install python3-dnspython python3-bs4
```

#### Operation

It has a few inputs:

- A manual list of sites defined in the 'mysites' var
- A manual list of domains defined in the 'domains' var
- A CSV file downloaded from moz.com with the top 500 websites
- A manual list of top-level-domains to ignore defined in the 'ignore_tlds' var

For the sites in the manual list and the top 500 CSV it makes a connection to 
each over HTTP, and gets the resulting HTML.  If a domain in the top 500 list 
is under a top-level domain from 'ignore_tlds' it skips it, however.  For pages 
downloaded, it parses the HTML looking for links, and adds any domains in those 
links to the 'domains' list.

Finally it makes both an A-record and AAAA query for each domain on the 
resulting domain list.  It sleeps for 2 seconds between each query to not 
hammer the resolver too hard, and spread the queries over time.
 
#### Systemd

It takes about 25 minutes to run given the delays between queries.  I run it
automatically every 60 minutes using a systemd timer.  The unit files for the 
service and timer I used can be found in the systemd directory.
