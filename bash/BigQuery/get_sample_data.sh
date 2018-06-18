#!/bin/bash

# const.
SQL_LIST=./sql_list.txt
RESULT=./result.tsv

# init RESULT
cat /dev/null > ${RESULT}

# get sample data for BigQuery
while read row;
  do
    echo `bq query --nouse_legacy_sql --format csv "${row}" | sed "2 d"` | tr "," "\\t" >> ${RESULT}
  done < ${SQL_LIST}
