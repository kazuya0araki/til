#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import time
import psycopg2
import yaml
import csv


# check sys.argv
argv_count = len(sys.argv)
if argv_count != 3:
    print("Usage: # python %s connection_congig_filename sql_filename" % sys.argv[0])
    quit()

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
    # start logging
    start_time = time.time()
    print("start execute sql.")

    # read SQL
    sql = open(sql_filename).read()

    # connect to Redshift
    connection = psycopg2.connect("host=" + HOST
                                  + " port=" + PORT
                                  + " dbname=" + DBNAME
                                  + " user=" + USER
                                  + " password=" + PASSWORD
                                  )

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

    # end logging
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("end!")
    print("elapsed time : {0}".format(elapsed_time) + "[sec]")


# main
def main():
    select(sys.argv[2])


if __name__ == '__main__':
    main()
