#!/usr/bin/python3

import nmap
import argparse


def print_scan(portscanner):
    
    for host in portscanner.all_hosts():
        print(f"{host}")
        
        for protocol in portscanner[host].all_protocols():
            ports = portscanner[host][protocol].keys()

            for port in ports:
                port_state = portscanner[host][protocol][port]['state']
                print(f"* {port}/{protocol} {port_state}") 

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Provide ip or network subnet to be scanned')
    args = parser.parse_args()
    

    target = args.target
    ps = nmap.PortScanner()
    ps.scan(hosts=target, arguments='')
    print_scan(ps)


if __name__ == "__main__":
    main()
