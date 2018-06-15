#!/bin/bash

# const.
SQL_LIST=./sql_list.txt
RESULT=./result.csv

# init RESULT
cat /dev/null > ${RESULT}

# get sample data for BigQuery
while read row;
  do
    echo `bq query --nouse_legacy_sql --format csv "${row}" | sed "2 d"` >> ${RESULT}
  done < ${SQL_LIST}
