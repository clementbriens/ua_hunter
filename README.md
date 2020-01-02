# ua_hunter


     _   _   ___       _   _  _   _  _   _  _____  _____ ______
    | | | | / _ \     | | | || | | || \ | ||_   _||  ___|| ___ \
    | | | |/ /_\ \    | |_| || | | ||  \| |  | |  | |__  | |_/ /
    | | | ||  _  |    |  _  || | | || . ` |  | |  |  __| |    /
    | |_| || | | |    | | | || |_| || |\  |  | |  | |___ | |\ \
     \___/ \_| |_/    \_| |_/ \___/ \_| \_/  \_/  \____/ \_| \_|
     
  
Reverse search Google Analytics codes on websites of interest to discover hidden links. Inspired by:

http://www.automatingosint.com/blog/2015/08/osint-discover-shared-tracking-code-between-domains/

https://globalvoices.org/2015/07/13/open-source-information-reveals-pro-kremlin-web-campaign/


## Setup

`git clone https://github.com/clementbriens/ua_hunter`

`cd ua_hunter`

`virtualenv env -p python3`

`pip install -r requirements.txt`

`source env/bin/activate`

Grab yourself an API key at https://publicwww.com/

## Usage

`python run.py -a YOUR_API_KEY -d MAIN_DOMAIN -r RECURSION_LIMIT`

The `recursion_limit` allows you to limit the number of scraped websites beyond your main domain, as the number of scraped can grow exponentially with Google Analytics codes.

The script outputs a .csv file named after your main domain input. The .csv file includes `parent_domain`, `child_domain`, and `UA_code`. This should allow you to conduct further network analysis using Gephi. 

## Future improvements

- Add direct integration with Networkx for Social Network Analysis
- Get Whois information on each domain
- Find a faster API
