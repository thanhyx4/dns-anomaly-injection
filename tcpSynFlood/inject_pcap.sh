#!/bin/bash
#bash inject_pcap.sh

INPUT="./input/"    #dns-hdns-02_2024-01-07_00_01.pcap.gz
OUTPUT="./output/"
NUM_PACKET=10           #numbers packets per second
INITIAL_TIME=0
DURATION=60             #seconds
ZOMBIES=10
WINDOWS=0.01            #window size
PPS=42                    #packets per window
SERVER="117.122.125.80"     #server ip


#each time read file -> create different botnets -> consuming time
#bash inject_pcap.sh "./input/*.pcap"     #must have ""


for filename in $1; do
    TMP="${OUTPUT}${filename:8:-3}"
    if [ -f "${TMP}" ]; then
      echo "Exist dir: ${TMP}"
      echo "Process next file"
      continue
    fi
    #TMP=$OUTPUT
	  COMMAND="python3 TCPMain.py -i ${filename} -o ${TMP}  -z 5 -it 60  -d 120 -s "203.119.73.80""
	  echo "${COMMAND}"
	  sh -c "${COMMAND}"
done