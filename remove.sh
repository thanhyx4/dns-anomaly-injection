#!/bin/bash

#bash testPcap.sh "./Port\ Scanning/output/*.pcap" "./Port\ Scanning/output/"


lst=("dnsFloodNXDOMAIN/input/*" "dnsFloodNXDOMAIN/output/*" "Amplificacion/input/*" "Amplificacion/output/*" "UDP\ Floods/input/*" "UDP\ Floods/output/*" "tcpSynFlood/input/*" "tcpSynFlood/output/*" "Port\ Scanning/input*" "Port\ Scanning/output*")
for i in "${lst[@]}"; do
  # shellcheck disable=SC2066
    COMMAND="rm -fr "$i""
    echo "${COMMAND}"
    sh -c "${COMMAND}"
done