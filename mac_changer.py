import subprocess
import optparse
import re

def mac_changer(interface,new_mac):
    print("[@+] Changing MAC address of "+ interface +" to "+ new_mac)
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"u"])

def arguments_input():
    praser = optparse.OptionParser()
    praser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address.")
    praser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    (options, arguments) = praser.parse_args()
    if not options.interaface :
        praser.error("[@-] Enter a valid interface.")
    elif not options.new_mac :
        praser.error("[@-] Enter a valid MAC adress.")
    return options

def check_mac(interface):
    result = subprocess.check_output(["ifconfig", interface])
    final = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)
    if final:
        return final.group(0)
    else:
        print("[@-] MAC address not found.")


options = arguments_input()
result = check_mac(options.interaface)
print("[@*] Current MAC address : "+ str(result))
mac_changer(options.interaface,options.new_mac)
result = check_mac(options.interaface)
if result == options.new_mac:
    print("[@+] MAC address changed successfully : "+ result)
else:
    print("[@-] MAC address not changed : " + result)