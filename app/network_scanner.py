#!/usr/bin/python3

import nmap
import argparse
import os
import pandas as pd
import datetime


def print_scan(portscanner):
    for host in portscanner.all_hosts():
        print(f"{host}")
        
        for protocol in portscanner[host].all_protocols():
            ports = portscanner[host][protocol].keys()

            for port in ports:
                port_state = portscanner[host][protocol][port]['state']
                print(f"* {port}/{protocol} {port_state}") 

def main():

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    output_filename_previous = 'scan_previous.csv'
    output_filename_current = 'scan_current.csv'
    output_filename_diff = f'scan_diff_{current_time}.csv'

    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Provide ip or network subnet to be scanned')
    args = parser.parse_args()
    

    target = args.target
    ps = nmap.PortScanner()
    ps.scan(hosts=target, arguments='')
    print_scan(ps)
   
    # We do not have previous scan result
    if os.path.isfile(f"./{output_filename_previous}") is not True:
        print(' --> Previous scan output does not exist, creating one')
        
        with open(output_filename_previous, 'w') as f:
            f.write(ps.csv())

    # We have previous scan result 
    else:
        print(' --> Previous scan exists, comparing agains current one')
        with open(output_filename_current, 'w') as f:
            f.write(ps.csv())
            
        previous_scan = pd.read_csv(output_filename_previous, sep=';')
        current_scan = pd.read_csv(output_filename_current, sep=';')
        
        # Compare scans
        diff = pd.concat([previous_scan, current_scan]).drop_duplicates(keep=False)
        
        if diff.empty:
            print(" --> No diff since last scan")
            
        else:
            print(" --> Diff since last scan !!! ")
            print("------------------------------")
            print(diff.to_string(index=False))
            print("------------------------------")
            
            print(f" --> Saving diff to {output_filename_diff}")
            diff.to_csv(output_filename_diff, sep=';', index=False)
            print(f" --> Saving current scan as previous scan")
            current_scan.to_csv(output_filename_previous, sep=';', index=False)


if __name__ == "__main__":
    main()
