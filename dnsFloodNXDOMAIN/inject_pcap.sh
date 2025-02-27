#!/bin/bash
#bash inject_pcap.sh

INPUT="./input/"    #dns-hdns-02_2024-01-07_00_01.pcap.gz
OUTPUT="./output/"
NUM_PACKET=10
INITIAL_TIME=0
DURATION=60
ZOMBIES=1
WINDOWS=0.01
PPS=42
SERVER="117.122.125.80"

#each time read file -> create different botnets -> consuming time
#bash inject_pcap.sh "*.pcap"     #must have ""


for filename in $1; do
    TMP="${OUTPUT}${filename:8:-3}"
    if [ -f "${TMP}" ]; then
      echo "Exist dir: ${TMP}"
      echo "Process next file"
      continue
    fi
    #TMP=$OUTPUT
	  COMMAND="python3 DNSMain.py -i ${filename} -o ${TMP} -z 5 -n 5 -it 0 -p 10 -d 120 -d 300 -s "203.119.73.80""
	  sh -c "${COMMAND}"
done