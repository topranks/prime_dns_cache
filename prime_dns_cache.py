#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re
import socket
import time
import dns.resolver

import sys

def main():
    ignore_tlds = set(['de', 'fr', 'jp', 'kr', 'au', 'sg', 'br', 'cn', 'it', 'nl',
        'sk', 'tw', 'ru', 'nz', 'pl', 'gov', 'in', 'es', 'ca'])

    mysites = [
        'news.bbc.co.uk',
        'www.theguardian.com',
        'news.ycombinator.com',
        'www.irishtimes.com',
        'www.independent.ie',
        'www.thejournal.ie',
        'www.newscientist.com',
        'www.reddit.com',
        'www.yahoo.co.uk',
        'www.wikipedia.org',
        'mail.yahoo.co.uk',
        'teams.microsoft.com',
        'office.com',
        'officeapps.live.com',
        'login.microsoftonline.com',
        'login.windows.net',
        'miro.com',
        'officeclient.microsoft.com',
        'outlook.office365.com'
        'outlook.office.com',
        'substrate.office.com',
        'track.realtimeboard.com',
        'lencr.org',
        'www.rottentomatoes.com',
        'theatlantic.com'
    ]

    domains = set([
        'aria.microsoft.com',
        'sentry-cdn.com',
        'office.net',
        'cdn.branch.io',
        'ocsp.digicert.com',
        'officecdn.microsoft.com.edgesuite.net',
        'outlook.office365.comoutlook.office.com',
        'sfbassets.com',
    ])

    i = 1
    for site in mysites:
        print(f"{i:<3} Getting {site} by HTTPS...", flush=True)
        i += 1
        domains.update(getSite(site))
        time.sleep(2)

    # Global top 500 list - can't be downloaded easily with rquests
    # https://moz.com/top-500/download/?table=top500Domains
    with open('top500Domains.csv', 'r') as csv_file:
        for line in csv_file.readlines():
            tokens = line.split(",")
            if len(tokens) > 2:
                domain = tokens[1].replace('"', '')
                tld = domain.split(".")[-1]
                if tld not in ignore_tlds:
                    print(f"{i:<3} Getting {domain} by HTTPS...", flush=True)
                    i += 1
                    domains.update(getSite(domain))
                    time.sleep(2)

    for domain in domains:
        tld = domain.split(".")[-1]
        if tld not in ignore_tlds:
            try:
                print(dns.resolver.resolve(domain, 'A').rrset, flush=True)
                print(dns.resolver.resolve(domain, 'AAAA').rrset, flush=True)
                time.sleep(2)
            except:
                pass


def getSite(site):
    # Get the site with HTTP:
    try:
        with requests.get("https://{}".format(site), timeout=(2, 4)) as r:
            site_html = r
    except Exception as e:
        print(f"Couldn't get {site} - {e}.", flush=True)
        return set([])

    soup = BeautifulSoup(site_html.text, 'html.parser')
    site_domains = set([])
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        domain = link.get('href').split("/")[2].split("?")[0]
        if domain != site:
           site_domains.add(domain)
    
    return(site_domains)


if __name__ == "__main__":
    main()

