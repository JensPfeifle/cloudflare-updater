import requests
import subprocess
import json
import sys

##################
# DNS API Basics
##################
# Create DNS record
# POST https://api.cloudflare.com/client/v4/zones/{api}/dns_records
# List DNS Records
# GET https://api.cloudflare.com/client/v4/zones/{api}/dns_records
# DNS record details
# GET https://api.cloudflare.com/client/v4/zones/{api}/dns_records/:identifier
# Update DNS record
# PUT https://api.cloudflare.com/client/v4/zones/{api}/dns_records/:identifier
# Delete DNS record
# DELETE https://api.cloudflare.com/client/v4/zones/{api}/dns_records/:identifier


##############
#  Settings
##############
# Get CF API Key: https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-
CF_API_KEY = ''
# cloudflare email address
CF_EMAIL = ''
# zone id is located on the main cloudflare domain dashboard
ZONE_ID = ''
# cloudflare dns record ID
RECORD_ID = ''  # AAAA www.jens.tech

DIG_BIN = '/usr/bin/dig'


def get_ipv6():
    raw_result = subprocess.check_output([DIG_BIN, '@resolver1.opendns.com', 'AAAA',
                                          'myip.opendns.com', '+short'])
    ipv6 = raw_result.decode().strip()
    return ipv6


def get_cf_records():
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(
            ZONE_ID),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    print(json.dumps(resp.json(), indent=4, sort_keys=True))
    sys.exit(0)


def cf_record_inspect(prop: str = 'content'):
    """ prop can be:
        id, type, name, contant, prxiable, proxied, ttl, locked, zone_id, zone_name, etc.
    """
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            ZONE_ID,
            RECORD_ID),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    if resp.status_code == 200:
        record_content = resp.json()['result'][prop]
        return record_content
    else:
        print('error in response {}'.format(resp))
        sys.exit(0)


def cf_record_update(rtype: str, name: str, content: str, proxied: bool):
    """ update the [rtype] [name] to containt [content]."""

    resp = requests.put(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            ZONE_ID,
            RECORD_ID),
        json={
            'type': rtype,
            'name': name,
            'content': content,
            'proxied': proxied
        },
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    return resp.status_code  # 200 on success


if __name__ == "__main__":

    oldip = cf_record_inspect(prop='content')
    newip = get_ipv6()

    if oldip == newip:
        print('no change ({})'.format(newip))
    else:
        result = cf_record_update('AAAA', 'www', newip, True)
        #result = 200

        if result == 200:
            print('updated dns record from {} to {}'.format(oldip, newip))
        else:
            print("request returned status code {}".format(result))
