import nmap


def print_scan(portscanner):
    
    for host in portscanner.all_hosts():
        print(f"{host}")
        
        for protocol in portscanner[host].all_protocols():
            ports = portscanner[host][protocol].keys()

            for port in ports:
                port_state = portscanner[host][protocol][port]['state']
                print(f"* {port}/{protocol} {port_state}") 

def main():

    target = '127.0.0.1'
    ps = nmap.PortScanner()
    ps.scan(hosts=target, arguments='')
    print_scan(ps)


if __name__ == "__main__":
    main()
