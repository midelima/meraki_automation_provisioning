
import meraki
import sys

# This uses Meraki Python SDK
# Make sure the MERAKI_DASHBOARD_API_KEY variable environment is defined

dashboard = meraki.DashboardAPI()

# Functions
def getorgid():
        my_orgs = dashboard.organizations.getOrganizations()
        for org_name in my_orgs:
                print(org_name['name'])

        org = input("Enter the organization name")

        for org_name in my_orgs:
                if org_name['name'] == org:
                        return org_name['id']
        return('null')

def createnetwork(org_id, site_code):
        ntw_name = format(str(site_code + "_Branch"))
        ntw_type = ["wireless", "appliance", "switch", "systemsManager", "camera", "cellularGateway", "environmental"]
        dashboard.organizations.createOrganizationNetwork(org_id, ntw_name, ntw_type)
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
        subnet = format(str("10." + site_code + ".10.0/24"))
        applianceip = format(str("10." + site_code + ".10.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "10", "DATA", subnet, applianceip)

        # VLAN20
        subnet = format(str("10." + site_code + ".20.0/24"))
        applianceip = format(str("10." + site_code + ".20.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "20", "VOICE", subnet, applianceip)

        # VLAN30
        subnet = format(str("10." + site_code + ".30.0/24"))
        applianceip = format(str("10." + site_code + ".30.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "30", "WLAN-CORP", subnet, applianceip)

        # VLAN40
        subnet = format(str("10." + site_code + ".40.0/24"))
        applianceip = format(str("10." + site_code + ".40.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "40", "WLAN-GUEST", subnet, applianceip)

        # VLAN90
        subnet = format(str("10." + site_code + ".90.0/24"))
        applianceip = format(str("10." + site_code + ".90.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "90", "MGMT", subnet, applianceip)

        # VLAN100
        subnet = format(str("10." + site_code + ".100.0/24"))
        applianceip = format(str("10." + site_code + ".100.254"))
        dashboard.appliance.createNetworkApplianceVlan(ntw_id, "100", "INX_ROUTER", subnet, applianceip)

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
        dashboard.appliance.createNetworkApplianceStaticRoute(ntw_id, "MPLS_ROUTE", "172.16.0.0/12", gtwip)
        return ('success')

# Main
def main(argv):

        print("This creates a Combined Network and configure the network based on a code site")
        print("Configuration will include VLANs, Static routes, DHCP and Firewall rules")

        orgid = getorgid()
        sitecode = input("Enter the site code :")
        ntwid = createnetwork(orgid, sitecode)
        createvlans(ntwid, sitecode)
        createfwrules(ntwid, sitecode)
        createstaticroute(ntwid, sitecode)

if __name__ == '__main__':
    main(sys.argv[1:])
