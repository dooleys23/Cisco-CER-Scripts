# CER API Requires SHA256 password rather than plaintext. This was implemented from 10.x to 11.x.
# Be careful, as the SSL verification is set to False.
# Use code at your own discretion

import requests, code
from xml.etree import ElementTree as ET

def main():
    primary_dc_list = []
    backup_dc_list = []

    # Gather all subnets into one dic
    master_subnet_dic = {}

    # Used for DC2 IP reference, could be improved
    ip_loop_counter = 0

    # for ip in primary_dc_list:
    for ip in primary_dc_list:

        # Get primary CER API XML
        r = requests.get('https://{0}/cerappservices/export/ipsubnet/info/username/password'.format(ip),
            verify=False)

        # Parsed XML content in dic format
        root = ET.fromstring(r.text)

        # Check if Pub.
        if 'Cannot fetch information from subscriber' in root[0].text:

            # Get backup CER API XML
            r = requests.get(
                'https://{0}/cerappservices/export/ipsubnet/info/username/password'.format(
                    backup_dc_list[ip_loop_counter]), verify=False)

            # Parsed XML content in dic format
            root = ET.fromstring(r.text)

        # Begins parsing
        if root[0].text == 'Exporting info':

            for subnet in root.iter('subnetdetails'):
                # master_subnet_dic[subnet] = [cer cluster, subnet mask, location]
                master_subnet_dic[subnet[0].text] = [primary_dc_list[ip_loop_counter], subnet[1].text, subnet[4].text]

        else:

            print('Was unable to reach backup IP. Please investigate')
            code.interact(local=locals())

        ip_loop_counter += 1

    with open('master_subnet_output.csv') as f:
        for subnet in master_subnet_dic:
            f.write('{},{}'.format(subnet, master_subnet_dic(subnet)))

main()
