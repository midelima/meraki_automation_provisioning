
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

def createnetwork(org_id, i):
        ntw_name = format(str("Branch_"+ str(i)))
        ntw_type = ["wireless", "appliance", "switch", "systemsManager", "camera", "cellularGateway", "environmental"]
        param = {
                'tags' : [format(str("n_"+ str(i)))]
        }
        dashboard.organizations.createOrganizationNetwork(org_id, ntw_name, ntw_type, **param)
        print("Creating the network…")

        ntw = dashboard.organizations.getOrganizationNetworks(org_id)
        for ntwid in ntw:
                if ntwid['name'] == ntw_name:
                        return ntwid['id']
        return('success')

def changelan(ntw_id, i):
        print("Changing LAN IP Subnet")
        if i < 256 :
                param = {
                        'subnet' : format(str("10.0."+ str(i)+".0/24")),
                        'applianceIp' : format(str("10.0."+ str(i)+".254"))
                }
        elif i >= 256 and i < 512 :
                param = {
                        'subnet' : format(str("10.1."+ str(i-256)+".0/24")),
                        'applianceIp' : format(str("10.1."+ str(i-256)+".254"))
                }
        elif i >= 512 and i < 768 :
                param = {
                        'subnet' : format(str("10.2."+ str(i-512)+".0/24")),
                        'applianceIp' : format(str("10.2."+ str(i-512)+".254"))
                }
        elif i >= 768 and i < 1024 :
                param = {
                        'subnet' : format(str("10.3."+ str(i-768)+".0/24")),
                        'applianceIp' : format(str("10.3."+ str(i-768)+".254"))
                }
        elif i >= 1024 and i < 1280 :
                param = {
                        'subnet' : format(str("10.4."+ str(i-1024)+".0/24")),
                        'applianceIp' : format(str("10.4."+ str(i-1024)+".254"))
                }
        elif i >= 1280 and i < 1536 :
                param = {
                        'subnet' : format(str("10.5."+ str(i-1280)+".0/24")),
                        'applianceIp' : format(str("10.5."+ str(i-1280)+".254"))
                }
        dashboard.appliance.updateNetworkApplianceSingleLan(ntw_id,**param)

        return ('success')


def enablevpn(ntw_id, i):
        print("Enabling VPN")
        if i < 256 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.0."+ str(i)+".0/24")), 'useVpn': True}]
                }
        elif i >= 256 and i < 512 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.1."+ str(i-256)+".0/24")), 'useVpn': True}]
                }
        elif i >= 512 and i < 768 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.2."+ str(i-512)+".0/24")), 'useVpn': True}]
                }
        elif i >= 768 and i < 1024 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.3."+ str(i-768)+".0/24")), 'useVpn': True}]
                }
        elif i >= 1024 and i < 1280 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.4."+ str(i-1024)+".0/24")), 'useVpn': True}]
                }
        elif i >= 1280 and i < 1536 :
                param = {
                        'subnets': [{'localSubnet': format(str("10.5."+ str(i-1280)+".0/24")), 'useVpn': True}]
                }
        mode = "hub"
        dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(ntw_id, mode, **param)

        return ('success')


def enable3rdpartyvpn(orgid, iteration):
        print("Configuring NM-VPN")
        param = {
                'peers': [{'name': format(str("EUR_"+ str(i))), 'publicIp': '45.15.204.101', 'privateSubnets': ['0.0.0.0/0'], 'secret': 'MerakiEurope!', 'ikeVersion': '2', 'networkTags': [format(str("n_"+ str(i)))], 'myUserFqdn': 'homesig78@2502110-512139444-umbrella.com', 'ipsecPoliciesPreset': 'aws'} for i in range(1,iteration+1)]
        }
        dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(orgid, **param)


        return ('success')



# Main
def main(argv):

        print(dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers('741405088655870450'))
        print("This script offers a bulk provisioning for networks and NM-VPN S2S configurations")

        orgid = getorgid()
        iteration = int(input("Enter the number of networks and NM-VPN S2S to be created : "))
        for i in range(1003,iteration+1) :
               print("i= " + str(i))
               print("iteration= "+ str(iteration))
               ntwid = createnetwork(orgid, i)
               print(ntwid)
               #ntwtag getnetworktag(ntwid)
               time.sleep(2)
               changelan(ntwid, i)
               enablevpn(ntwid, i)
               time.sleep(1)
        enable3rdpartyvpn(orgid, iteration)
        return ('success')

if __name__ == '__main__':
    main(sys.argv[1:])
