
import meraki
import sys
import requests
import json
import os

# This script uses Meraki Python SDK
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

# In case a clone from an existing network is not needed, make sure to removed the "copyFromNetworkID" field below.
# If you would like to clone from an existing network, please add the networkid below of the network to be cloned and check that network types are correct.
def createnetwork(org_id, site_code):
        ntw_name = format(str("Branch_"+ str(site_code)))
        ntw_type = ['wireless', 'appliance', 'switch', 'systemsManager', 'camera', 'sensor', 'cellularGateway']
        param = {
                'tags' : [format(str("n_"+ str(site_code)))],
                'timezone' : "Europe/Paris",
                'copyFromNetworkId' : "xxxxx",
                'notes' : "Combined network demo"
        }
        dashboard.organizations.createOrganizationNetwork(org_id, ntw_name, ntw_type, **param)
        print("Creating the network…")

        ntw = dashboard.organizations.getOrganizationNetworks(org_id)
        for ntwid in ntw:
                if ntwid['name'] == ntw_name:
                        return ntwid['id']
        return('null')

def createvlans(ntw_id, site_code):
        print("Configuring VLANs")
        dashboard.appliance.updateNetworkApplianceVlansSettings(ntw_id, vlansEnabled=True)

        #VLAN10
        param = {
                'subnet' : format(str("10." + site_code + ".10.0/24")),
                'applianceIp' : format(str("10." + site_code + ".10.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "10", "DATA", **param)


        # VLAN20
        param = {
                'subnet' : format(str("10." + site_code + ".20.0/24")),
                'applianceIp' : format(str("10." + site_code + ".20.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "20", "VOICE", **param)
        

        # VLAN30
        param = {
                'subnet' : format(str("10." + site_code + ".30.0/24")),
                'applianceIp' : format(str("10." + site_code + ".30.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "30", "WLAN-CORP", **param)


        # VLAN40
        param = {
                'subnet' : format(str("10." + site_code + ".40.0/24")),
                'applianceIp' : format(str("10." + site_code + ".40.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "40", "WLAN-GUEST", **param)


        # VLAN90
        param = {
                'subnet' : format(str("10." + site_code + ".90.0/24")),
                'applianceIp' : format(str("10." + site_code + ".90.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "90", "MGMT", **param)
        

        # VLAN100
        param = {
                'subnet' : format(str("10." + site_code + ".100.0/24")),
                'applianceIp' : format(str("10." + site_code + ".100.254"))
        }
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "100", "INX_ROUTER", **param)


        # DELETE VLAN 1
        dashboard.appliance.deleteNetworkApplianceVlan(ntw_id, "1")

        return ('success')

def createfwrules(ntw_id, site_code):
        print("Configuring Firewall Rules")

        dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                ntw_id,
                rules=[
                                {
                                        "comment": "Block WIFI_GUEST to LAN",
                                        "policy": "deny",
                                        "protocol": "Any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".40.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "10.0.0.0/8,172.16.0.0/12, 192.168.0.0/16",
                                },
                                {
                                        "comment": "Allow WIFI_GUEST to Internet only",
                                        "policy": "allow",
                                        "protocol": "tcp",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".40.0/24")),
                                        "destPort": "53,80,443",
                                        "destCidr": "Any",
                                },
                                {
                                        "comment": "Allow WIFI_GUEST to Internet only",
                                        "policy": "allow",
                                        "protocol": "udp",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".40.0/24")),
                                        "destPort": "53",
                                        "destCidr": "Any",
                                },
                                {
                                        "comment": "Allow VOICE to Collab resources",
                                        "policy": "allow",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".20.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.240.0/24",
                                },
                                {
                                        "comment": "Block VISIO to other DC resources",
                                        "policy": "deny",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".20.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.0.0/12",
                                },
                                {
                                        "comment": "Allow CORP Users to DC Hosted Business Apps",
                                        "policy": "allow",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".10.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.230.0/24",
                                },
                                {
                                        "comment": "Block CORP Users to other DC resources",
                                        "policy": "deny",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".10.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.0.0/12",
                                },
                                {
                                        "comment": "Allow MGMT to access DC monitoring tools",
                                        "policy": "allow",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".90.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.220.0/24",
                                },
                                {
                                        "comment": "Block MGMT to access other DC resources",
                                        "policy": "deny",
                                        "protocol": "any",
                                        "srcPort": "Any",
                                        "srcCidr": format(str("10." + str(site_code) + ".90.0/24")),
                                        "destPort": "Any",
                                        "destCidr": "172.16.0.0/12",
                                }
                        ]
        )
        return ('success')

def createstaticroute(ntw_id, site_code):
        gtwip = format(str("10." + str(site_code) + ".100.1"))
        dashboard.appliance.createNetworkApplianceStaticRoute(ntw_id, "INX_ROUTE", "172.16.0.0/12", gtwip)
        return ('success')

# Uncomment function below if you would like to add devices as part of your demo
# Also uncomment the function in the main below and adapt your sn
# def adddevices(ntw_id, sn_ms, sn_mr, sn_mx):
#         url = "https://api.meraki.com/api/v1/networks/"+format(str(ntw_id))+"/devices/claim"
#         print(url)
        
#         payload = json.dumps({
#             "serials": [
#                 sn_mx,
#                 sn_ms,
#                 sn_mr
#             ]
#         })

#         headers = {
#           'X-Cisco-Meraki-API-Key': '852f16c2ceb0f3529784e363a414f92f883a2289',
#           'Content-Type': 'application/json'
#         }

#         response = requests.request("POST", url, headers=headers, data=payload)
#         print("Devices added successfully")

#         return ('success')

# Uncomment and adapt function below if you would like to configure switchports as part of your demo
# Also uncomment the function in the main below and adapt your sn
# def confswitchport(sn_ms):
#         update_switchport = dict(serial=sn_ms,
#                                  portId='1',
#                                  name='AP',
#                                  tags=['WIFI'],
#                                  enabled='true',
#                                  type='trunk',
#                                  vlan='1',
#                                  voiceVlan='20',
#                                  allowedVlans='1-1000',
#                                  isolationEnabled='false',
#                                  rstpEnabled='true',
#                                  stpGuard='disabled',
#                                  linkNegotiation='Auto negotiate',
#                                  portScheduled='null',
#                                  udld='Alert only',
#                                  linkNegotiationCapabilities='Auto negotiate',
#                                  accessPolicyType='Open'
#                                 )
#         dashboard.switch.updateDeviceSwitchPort(**update_switchport)
#         update_switchport = dict(serial=sn_ms,
#                                  portId='2',
#                                  name='MV',
#                                  tags=['Camera'],
#                                  enabled='true',
#                                  type='access',
#                                  vlan='90',
#                                  voiceVlan='20',
#                                  allowedVlans='1-1000',
#                                  isolationEnabled='false',
#                                  rstpEnabled='true',
#                                  stpGuard='disabled',
#                                  linkNegotiation='Auto negotiate',
#                                  portScheduled='null',
#                                  udld='Alert only',
#                                  linkNegotiationCapabilities='Auto negotiate',
#                                  accessPolicyType='Open'
#                                 )
#         dashboard.switch.updateDeviceSwitchPort(**update_switchport)
#         print("Port 3 configured successfully")
#         update_switchport = dict(serial=sn_ms,
#                                  portId='3',
#                                  name='PC',
#                                  tags=['PC'],
#                                  enabled='true',
#                                  type='access',
#                                  vlan='10',
#                                  voiceVlan='20',
#                                  allowedVlans='1-1000',
#                                  isolationEnabled='false',
#                                  rstpEnabled='true',
#                                  stpGuard='disabled',
#                                  linkNegotiation='Auto negotiate',
#                                  portScheduled='null',
#                                  udld='Alert only',
#                                  linkNegotiationCapabilities='Auto negotiate',
#                                  accessPolicyType='Custom access policy',
#                                  accessPolicyNumber='1'
#                                 )
#         dashboard.switch.updateDeviceSwitchPort(**update_switchport)
#         print("Port 3 configured successfully")

#         return ('success')

# Main
def main(argv):

        print("This creates a Combined Network and configure the network based on a code site")
        print("Configuration will include VLANs, Static routes, DHCP and Firewall rules")
        sn_mx = format(str("xxxx-xxxx-xxxx"))
        sn_ms = format(str("xxxx-xxxx-xxxx"))
        sn_mr = format(str("xxxx-xxxx-xxxx"))

        orgid = getorgid()
        sitecode = input("Enter the site code :")
        ntwid = createnetwork(orgid, sitecode)
        createvlans(ntwid, sitecode)
        createfwrules(ntwid, sitecode)
        createstaticroute(ntwid, sitecode)
        #adddevices(ntwid, sn_ms, sn_mr, sn_mx)
        #confswitchport(sn_ms)

if __name__ == '__main__':
    main(sys.argv[1:])
