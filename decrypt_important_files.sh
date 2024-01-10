#!/bin/bash

bigquery_keyfile="$(pwd)/dbs/servers/bigquery/bigquery1/tokens/bigquery-token.json"
redshift_keyfile="$(pwd)/dbs/servers/redshift/test_data/tokens/redshift_iam.json"

#create keys if needed and decrypt key files.
[ $(gpg --list-keys | grep -c $(whoami)) -eq 0 ] && gpg --gen-key --no-tty

redshift_keyfile_dc="$(pwd)/dbs/servers/redshift/test_data/tokens/redshift_iam.json.gpg"
bigquery_keyfile_dc="$(pwd)/dbs/servers/bigquery/bigquery1/tokens/bigquery-token.json.gpg"

if [ ! -f "$redshift_keyfile" ]; then
    gpg --no-tty -d "$redshift_keyfile_dc" > "$redshift_keyfile"
fi

if [ ! -f "$bigquery_keyfile" ]; then
    gpg --no-tty -d "$bigquery_keyfile_dc" > "$bigquery_keyfile"
fi


echo "end of decryption"


if [ -f "$bigquery_keyfile_dc" ]; then
    rm -rf $bigquery_keyfile_dc
fi

if [ -f "$redshift_keyfile_dc" ]; then
    rm -rf $redshift_keyfile_dc
fi

#end of key creation. ...