#!/bin/bash
#bash inject_pcap.sh

INPUT="./input/"    #dns-hdns-02_2024-01-07_00_01.pcap.gz
OUTPUT="./output/"
NUM_PACKET=10           #numbers packets per second
INITIAL_TIME=0
DURATION=60             #seconds
ZOMBIES=1
WINDOWS=0.01            #window size
PPS=42                    #packets per window
SERVER="117.122.125.80"     #server ip
SourceP=21517

#each time read file -> create different botnets -> consuming time
#bash inject_pcap.sh "*.pcap"     #must have ""
#required paremeters
TARGET="8.8.8.8"
DOMAIN="vnnic.vn"

for filename in $1; do
    TMP="${OUTPUT}${filename:8:-3}"
    if [ -f "${TMP}" ]; then
      echo "Exist dir: ${TMP}"
      echo "Process next file"
      continue
    fi
    #TMP=$OUTPUT
	  COMMAND="python3 mainAmplification.py -i ${filename} -o ${TMP} -target ${TARGET} -dom ${DOMAIN} -z 5 -it 0  -d 120 -rtype $true -s "203.119.73.80""
	  echo "${COMMAND}"
	  sh -c "${COMMAND}"
done