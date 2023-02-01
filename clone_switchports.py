import meraki
import sys
import requests
import json
import time
import os

# This uses Meraki Python SDK
# Make sure the MERAKI_DASHBOARD_API_KEY variable environment is defined
# This script has been built to close MS350-24X to MS390-24P. Other models will require changes.

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
    return ('null')


def getnetwork(org_id):
    my_ntws = dashboard.organizations.getOrganizationNetworks(org_id)
    for ntw_name in my_ntws:
        print(ntw_name['name'])
    ntw = input("Enter the network name : ")

    for ntwid in my_ntws:
        if ntwid['name'] == ntw:
            return ntwid['id']
    return ('success')


def getswsource(ntwid):
    my_sws = dashboard.networks.getNetworkDevices(ntwid)
    for sw_sn in my_sws:
        print(sw_sn['serial'])
    sw_source_sn = input("Enter the serial number of the source switch : ")
    return sw_source_sn

def getswdest(ntwid):
    my_sws = dashboard.networks.getNetworkDevices(ntwid)
    for sw_sn in my_sws:
        print(sw_sn['serial'])
    sw_source_sn = input("Enter the serial number of the destination switch : ")
    return sw_source_sn

def getswitchportssrc(sn_source):
    my_sws = dashboard.networks.getNetworkDevices(ntwid)
    for sw_sn in my_sws:
        print(sw_sn['serial'])
    sw_source_sn = input("Enter the serial number of the destination switch : ")
    return sw_source_sn

def clonesw(sn_src, sn_dst):
    switchports = dashboard.switch.getDeviceSwitchPorts(sn_src)
    if len(switchports) == 30: # 24 ports switch
        model_sw = [i for i in range(25)]
        model_string = map(str, model_sw)
        for switchport in switchports:
            if switchport["portId"] in model_string:
                if switchport["allowedVlans"] == "all" and switchport["type"] == "trunk":
                    update_switchport = dict(serial=sn_dst,
                                             portId=switchport["portId"],
                                             name=switchport['name'],
                                             tags=switchport['tags'],
                                             enabled=switchport["enabled"],
                                             type=switchport["type"],
                                             vlan=switchport["vlan"],
                                             voiceVlan=switchport["voiceVlan"],
                                             allowedVlans="1-1000",
                                             isolationEnabled=switchport["isolationEnabled"],
                                             rstpEnabled=switchport["rstpEnabled"],
                                             stpGuard=switchport["stpGuard"],
                                             linkNegotiation=switchport["linkNegotiation"],
                                             portScheduled=switchport["portScheduleId"],
                                             udld=switchport["udld"],
                                             linkNegotiationCapabilities=switchport["linkNegotiationCapabilities"],
                                             accessPolicyType=switchport["accessPolicyType"]
                                             )
                    if update_switchport['accessPolicyType'] != "Open":
                        update_switchport['accessPolicyNumber'] = switchport['accessPolicyNumber']
                else:
                    update_switchport = dict(serial=sn_dst,
                                             portId=switchport["portId"],
                                             name=switchport['name'],
                                             tags=switchport['tags'],
                                             enabled=switchport["enabled"],
                                             type=switchport["type"],
                                             vlan=switchport["vlan"],
                                             voiceVlan=switchport["voiceVlan"],
                                             allowedVlans=switchport["allowedVlans"],
                                             isolationEnabled=switchport["isolationEnabled"],
                                             rstpEnabled=switchport["rstpEnabled"],
                                             stpGuard=switchport["stpGuard"],
                                             linkNegotiation=switchport["linkNegotiation"],
                                             portScheduled=switchport["portScheduleId"],
                                             udld=switchport["udld"],
                                             linkNegotiationCapabilities = switchport["linkNegotiationCapabilities"],
                                             accessPolicyType = switchport["accessPolicyType"]
                                             )
                    if update_switchport['accessPolicyType'] != "Open":
                        update_switchport['accessPolicyNumber'] = switchport['accessPolicyNumber']
                dashboard.switch.updateDeviceSwitchPort(**update_switchport)
                print("Configuring port "+switchport["portId"])
        print("Cloning du switch 24 ports "+sn_src+" vers le switch "+sn_dst+" terminé")
    elif len(switchports) == 54: # 48 ports switch
        model_sw = [i for i in range(49)]
        model_string = map(str, model_sw)
        for switchport in switchports:
            if switchport["portId"] in model_string:
                update_switchport = dict(serial=sn_dst,
                                  portId=switchport["portId"],
                                  name=switchport['name'],
                                  tags=switchport['tags'],
                                  enabled=switchport["enabled"],
                                  type=switchport["type"],
                                  vlan=switchport["vlan"],
                                  voiceVlan=switchport["voiceVlan"],
                                  allowedVlans=switchport["allowedVlans"],
                                  isolationEnabled=switchport["isolationEnabled"],
                                  rstpEnabled=switchport["rstpEnabled"],
                                  stpGuard=switchport["stpGuard"],
                                  linkNegotiation=switchport["linkNegotiation"],
                                  portScheduled=switchport["portScheduleId"],
                                  udld=switchport["udld"],
                                  linkNegotiationCapabilities = switchport["linkNegotiationCapabilities"],
                                  accessPolicyType = switchport["accessPolicyType"]
                                  )
                dashboard.switch.updateDeviceSwitchPort(**update_switchport)
                print("Configuring port "+switchport["portId"])
            print("Cloning du switch 48 ports "+sn_src+" vers le switch "+sn_dst+" terminé")
    else:
        print("Error during cloning procedure : the switch is not a regular MS 24/48 ports switch ")
    return ('success')


# Main
def main(argv):
    print("This script offers the ability to clone the MS switchports.")

    orgid = getorgid()
    ntwid = getnetwork(orgid)
    sn_source = getswsource(ntwid)
    sn_dest = getswdest(ntwid)
    clonesw(sn_source, sn_dest)

    return ('success')


if __name__ == '__main__':
    main(sys.argv[1:])
