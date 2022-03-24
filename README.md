# Network Scanner


## Description:
- Basic network port scanner that scan targer(ip / network) for open ports and print results.

- Scanner compares scan results against previous run if available.

- Diffs between scans are displayed if any and saved for later analysis.

<br/>

## Prerequisites
- python3

- nmap binaries has to be installed

- See python libraries requirements in requirements.txt

<br/>

## How to run:

To scan for open ports on host/network

`./network_scanner.py <target_host_ip>|<target_network/netmask>`

To see help

`./network_scanner.py`

or

`./network_scanner.py -h`

<br/>

## Example run:

**1.RUN (no previous scan output available):**

```
./network_scanner.py 127.0.0.1 
127.0.0.1
* 22/tcp open
* 111/tcp open
* 631/tcp open
* 902/tcp open
* 3306/tcp open
 --> Previous scan output does not exist, creating one
```

**2.RUN (previous scan output available):**
```
./network_scanner.py 127.0.0.1 
127.0.0.1
* 22/tcp open
* 111/tcp open
* 631/tcp open
* 902/tcp open
* 3306/tcp open
 --> Previous scan exists, comparing agains current one
 --> No diff since last scan
```

**3.RUN (a change has occurred):**

```
./network_scanner.py 127.0.0.1 
127.0.0.1
* 22/tcp open
* 111/tcp open
* 631/tcp open
* 902/tcp open
* 3306/tcp open
 --> Previous scan exists, comparing agains current one
 --> Diff since last scan !!! 
------------------------------
     host  hostname hostname_type protocol  port  name state  product  extrainfo  reason  version  conf  cpe
127.0.0.1 localhost           PTR      tcp  3306 mysql  open      NaN        NaN syn-ack      NaN     3  NaN
------------------------------
 --> Saving diff to scan_diff_20220320-134736.csv
 --> Saving current scan as previous scan
```
<br/>

## How to run inside container:

Docker needs to be installed.
<br/>


### Build container:

- in project's root with docker
```
docker build --tag msolcansk/network-scanner:latest .
```

or

- Use visual studio code:

Build and run config is in .vscode dir.

You will have to change "args" in tasks.json to appropriate target ip/network for your docker network setup 


<br/>

### Run container:
Run scan against target ip/network. You need to provide volume to store previous scan and scan diffs.


```
docker run --mount source=scanner_vol,target=/app/output msolcansk/network-scanner:latest <ip/network target>
```

Run scan against apache container in default Docker bridged network:
```
docker run --rm --mount source=scanner_vol,target=/app/output msolcansk/network-scanner:latest 172.17.0.2
```

Example test with running on docker host network (You do not have to have another container running in bridge network/other network) DO NOT RUN IN PROD!!!:

```
docker run --rm --network host msolcansk/network-scanner:latest 127.0.0.1 
```

<br/>


### Run on K8S(minikube):
```
kubectl create -f scanner.yaml
```