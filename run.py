import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-a","--api_key",    required=True,help="publicwww.com API key")
ap.add_argument("-d","--main_domain",      required=True,help="Master domain to recon.")
ap.add_argument("-r", "--recursion",required=True,help="Recursion level for recon.")

args = vars(ap.parse_args())


# api_key = '5cede677001d99db064959278cb331c4'
# main_domain = '4chan.org'
# recursion = 0

def get_codes(discovered_codes, domain):
    codes = []
    url = "https://" + domain
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    scripts = soup.find_all('script')
    for script in scripts:
        res = re.findall('UA-(.+?)-', str(scripts))
        for result in res:
            if result not in codes and result not in discovered_codes:
                codes.append(result)
                discovered_codes.append(result)
    print('[*] Found {} new Google Analytics code(s) on {}'.format(len(codes), domain))
    return codes


def get_domains(parent,codes):
    discovered_domains = []
    for code in codes:
        print()
        url = 'https://publicwww.com/websites/{}/?export=csvu&key={}'.format(code, args['api_key'])
        c = pd.read_csv(url)
        if len(c.values) > 100:
            print('[*] Too many websites using this code- skipping')
        else:
            print('[*] Found {} websites using {}'.format(len(c), code))
            for result in c.values:
                child_domain = result[0].split('/')[2]
                discovered_domains.append(child_domain)
                print('[*] --> {}'.format(child_domain))
                info = {
                'parent_domain' : parent,
                'child_domain' : child_domain,
                'UA_code' : code
                }
                sna_df.loc[len(sna_df)] = info
    return discovered_domains


def recursive_scrape(domains, recursion_level):
    if recursion_level < int(args['recursion']):
        for domain in domains:
            codes = get_codes(discovered_codes, domain)
            if codes:
                domains = get_domains(domain, codes)
            else:
                ['[*] No new codes found for {}'.format(domain)]
        recursion_level +=1
        recursive_scrape(domains, recursion_level)
    else:
        print('[*] Recursive limit hit. Stopping scrape.')




if __name__ == '__main__':
    print(r"""

     _   _   ___       _   _  _   _  _   _  _____  _____ ______
    | | | | / _ \     | | | || | | || \ | ||_   _||  ___|| ___ \
    | | | |/ /_\ \    | |_| || | | ||  \| |  | |  | |__  | |_/ /
    | | | ||  _  |    |  _  || | | || . ` |  | |  |  __| |    /
    | |_| || | | |    | | | || |_| || |\  |  | |  | |___ | |\ \
     \___/ \_| |_/    \_| |_/ \___/ \_| \_/  \_/  \____/ \_| \_|

     by clement briens

     Discover hidden links between disinfo websites using
     Google Analytics codes.




     """)
    discovered_codes = []
    sna_df = pd.DataFrame(columns=['parent_domain', 'child_domain', 'UA_code'])
    codes = get_codes(discovered_codes, args['main_domain'])
    if codes:
        domains = get_domains(args['main_domain'], codes)
        recursion_level = 0
        recursive_scrape(domains, recursion_level)
        sna_df.to_csv('{}.csv'.format(args['main_domain']))
        print('[*] Exported data to csv.')
    else:
        print('[*] No codes found.')
