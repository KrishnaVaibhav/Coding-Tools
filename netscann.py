import scapy.all as scapy
import optparse

def arguments():
    parse = optparse.OptionParser()
    parse.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    (options, args) = parse.parse_args()
    return options

def scan(ip):
    request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip)
    response = scapy.srp(request, timeout=1, verbose=False)[0]
    response_list=[]
    for e in response:
        response_dict = {"ip":e[1].psrc, "mac":e[1].hwsrc}
        response_list.append(response_dict)
    return response_list

def result(response_list):
    print("\tIP\t\t\tMAC Address\n--------------------------------------------------")
    for e in response_list:
        print(e["ip"]+ "\t\t\t" + e["mac"])

options = arguments()
scan_r = scan(options.target)
result(scan_r)