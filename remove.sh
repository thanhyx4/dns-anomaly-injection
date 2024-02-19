#!/bin/bash

lst=("dnsFloodNXDOMAIN/input/*" "dnsFloodNXDOMAIN/output/*" "Amplificacion/input/*" "Amplificacion/output/*" "UDP\ Floods/input/*" "UDP\ Floods/output/*" "tcpSynFlood/input/*" "tcpSynFlood/output/*")
for i in "${lst[@]}"; do
  # shellcheck disable=SC2066
    COMMAND="rm -fr "$i""
    echo "${COMMAND}"
    sh -c "${COMMAND}"
done