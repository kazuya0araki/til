#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import psycopg2
import yaml
import csv

# read config
yaml_f = open(sys.argv[1], "r+")
CONFIG = yaml.load(yaml_f)

# define connection
HOST = CONFIG["host"]
PORT = str(CONFIG["port"])
DBNAME = CONFIG["dbname"]
USER = CONFIG["user"]
PASSWORD = CONFIG["password"]


# SQL to CSV
def select(sql_filename):
    # read SQL
    sql = open(sql_filename).read()

    # connect to Redshift
    connection = psycopg2.connect("host=" + HOST + " port=" + PORT + " dbname=" + DBNAME + " user=" + USER + " password=" + PASSWORD)

    # execute SQL
    cur = connection.cursor()
    cur.execute(sql)
    column_names = [desc[0] for desc in cur.description]

    # output CSV
    with open("output.csv", "w", encoding="utf-8") as out:
        csv_writer = csv.writer(out, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(column_names)
        for row in cur:
            csv_writer.writerow(row)

    # close connection
    connection.close()


def main():
    select(sys.argv[2])


if __name__ == '__main__':
    main()
