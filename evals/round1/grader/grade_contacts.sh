#!/bin/bash
d=$1; G=$(dirname "$0"); out=$(mktemp)
s=$(date +%s.%N); (cd "$d" && python3 import_contacts.py data/contacts_big.csv "$out") ; e=$(date +%s.%N)
echo "runtime: $(echo "$e - $s" | bc)s"
cmp -s "$out" "$G/expected_big.csv" && echo "output identical: YES" || echo "output identical: NO"
