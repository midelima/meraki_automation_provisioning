
import meraki
import sys
import requests
import json
import time
import os

# This uses Meraki Python SDK
# Make sure the MERAKI_DASHBOARD_API_KEY variable environment is defined

api_key = os.environ.get('MERAKI_DASHBOARD_API_KEY')
if not api_key:
            raise APIKeyError()
dashboard = meraki.DashboardAPI()

# Functions
def getorgid():
        my_orgs = dashboard.organizations.getOrganizations()
        for org_name in my_orgs:
                print(org_name['name'])

        org = input("Enter the organization name : ")

        for org_name in my_orgs:
                if org_name['name'] == org:
                        return org_name['id']
        return('null')


def deletenetworks(orgid):
        my_networks = dashboard.organizations.getOrganizationNetworks(orgid)
        print("Are you sure to delete all networks below ?")
        for net_name in my_networks:
                print(net_name['name'])

        net = input("Yes or No\n")
        if net == "Yes":
                for net_name in my_networks:
                        dashboard.networks.deleteNetwork(net_name['id'])

        return ('success')



# Main
def main(argv):

        print(dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers('741405088655870450'))
        print("This script delete all networks in a specific organizations")

        orgid = getorgid()
        deletenetworks(orgid)
        return ('success')

if __name__ == '__main__':
    main(sys.argv[1:])
