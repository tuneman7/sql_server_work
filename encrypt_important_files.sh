#!/bin/bash

bigquery_keyfile="$(pwd)/dbs/servers/bigquery/bigquery1/tokens/bigquery-token.json"
redshift_keyfile="$(pwd)/dbs/servers/redshift/test_data/tokens/redshift_iam.json"

[ $(gpg --list-keys | grep -c $(whoami)) -eq 0 ] && gpg --gen-key --no-tty
gpg -e -r $(whoami) $bigquery_keyfile
gpg -e -r $(whoami) $redshift_keyfile

ls $bigquery_keyfile
ls $redshift_keyfile
rm $bigquery_keyfile
rm $redshift_keyfile
ls $bigquery_keyfile
ls $redshift_keyfile
