#!/bin/bash

echo "Create transactions/<uuid>.json form stdin"

mkdir -p transactions

while read line; do
  id="$(uuidgen)"
  content="{\
\n  \"id\": \"${id}\",\
\n  \"content\": \"${line}\",\
\n  \"links\": []\
\n}"
  echo -e "${content}" > transactions/${id}.json
done
