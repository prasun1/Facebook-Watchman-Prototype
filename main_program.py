import sys
from datetime import datetime, timedelta
import sqlite3
import os
import sys
from os import listdir
from glob import glob
from os.path import isfile, join
import time
import hashlib
import datetime
''' this function is used to traverse the database and gives output based on user input'''
def search(start,end,file_name,conn):
   cur = conn.cursor()
   if file_name is None:
        query = "SELECT fpath,fmtime,rectime FROM table_fscrawler  WHERE fmtime >= '" + start + "' AND rectime <= '" + end + "'"
   else:
        query = "SELECT fpath,fmtime,rectime FROM table_fscrawler  WHERE (fmtime >= '" + start + "' AND fmtime <= '" + end + "') AND fpath == '"+ file_name+"'"

   cur.execute(query)
   values = cur.fetchall()
   row_count = len(values)
   if row_count == 0:
        print("\033[1m" + "No data found in that time range\n")
        return
   print("\n" "\033[1m" + "Following files have been modified in the time range\n\n")
   titles = ['FilePath        \t ', 'ModifiedTime   \t      ', 'RecordedTime\t']
   data = [titles] + values

   for i, d in enumerate(data):
         line = '|'.join(str(x).ljust(20) for x in d)
         print(line)
         print("\n")
         if i == 0:
             print("-"*len(line))


def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Exception as e:
        print(e)
'''main method consist of all the validations of date and file entered by the user'''
if __name__ == "__main__":
    database = 'fscrawler'
    conn = create_connection(database)

    try:
       start_date = sys.argv[1]
       end_date = sys.argv[2]
       start_date_dateformat = datetime.datetime.strptime(start_date, "%Y-%m-%d")

       end_date_dateformat = datetime.datetime.strptime(end_date, "%Y-%m-%d")
       modified_date = end_date_dateformat + timedelta(days=1)
       end_date = datetime.datetime.strftime(modified_date, "%Y-%m-%d")
    except:
       print("Please enter the correct format: python <filename.py> startdate enddate filepath{optional}\n Date should be in the format of YYYY-MM-DD and filepath should be complete path of file not just the name")
    else:
       if start_date_dateformat > datetime.datetime.now():
               print("\nStart Date Cannot be future date. Please check the date\n")
       elif start_date > end_date:
               print("\nEnd date should be greater than start date\n")
       else:
            if len(sys.argv) == 4:
               file_name = sys.argv[3]
               
               search(start_date,end_date,file_name,conn)
            else:
               search(start_date,end_date,None,conn)
