#!/bin/bash
#bash testPcap.sh "./Amplification/output/*.pcap" ./Amplification/output/

COMMAND1="mergecap $1 -w - |dnsanalyzer -w 600  -i 600 -a 8 -p "both" -t 1.2 -P "srcIP" -c 25 -s 32 -g $2 -q  > "$2""anomaly_test.txt" "

echo "${COMMAND1}"
sh -c "${COMMAND1}" &
wait
COMMAND2="gnuplot "$2""*.gp""
sh -c "${COMMAND2}" &
wait
sh -c "mv "*.png" $2"                   #read from $1 move all png to $2
