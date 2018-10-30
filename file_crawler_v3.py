'''
version 3: Changes have been made regarding the main function. In place of single row, every change in file has been added to the database'''
import sqlite3
import os
import sys
from os import listdir
from glob import glob
from os.path import isfile, join
import datetime, time
import hashlib
import datetime

def file_crawler(path,search,conn):
    file_names, path_filenames, create_time, modified_time, hash_list, digests = list(),list(),list(),list(), list(),list()
    root_path = path.split('/')
    top_root = root_path[-1]
    present_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_obj = datetime.datetime.strptime(present_time, "%Y-%m-%d %H:%M:%S")
    '''
    #onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #used to print all files in a directory without nesting in other directory
#return onlyfiles
    '''
    print(path)
    if search == 'full':
        for path, subdirs, files in os.walk(path): # Used to print all files in the given directory and all its subdirectories
            for name in files:
                 file_names.append(name)
                 path_filenames.append(os.path.join(path, name))
    elif search == "top":
        top_files = [f for f in listdir(path) if isfile(join(path, f))]

        for name in top_files:
            file_names.append(name)
            path_filenames.append(os.path.join(path, name))

    '''In the function below, we are iterating over path_filenames list and calculating modfied time, hash of each file'''
    for k in path_filenames:
        create_time.append(time.ctime(os.path.getctime(k)))
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(k)))
        modified_datetime_obj = datetime.datetime.strptime(time_format, "%Y-%m-%d %H:%M:%S")
        modified_time.append(modified_datetime_obj)
        #hash_list.append(hashlib.sha256(k.encode('utf-8')).hexdigest())
        hasher = hashlib.md5()
        with open(k, 'rb') as f:
              buf = f.read()
              hasher.update(buf)
              a = hasher.hexdigest()
              digests.append(a)

    if_present = list()
    cur = conn.cursor()
    Flag = False
    '''iterating and inserting files in the database'''
    for i in range(len(path_filenames)):
        current_path = path_filenames[i]
        sql = '''SELECT fdigest FROM table_fscrawler t WHERE t.fpath=? ORDER  BY rectime DESC LIMIT  1;'''
        cur.execute(sql,(current_path,))

        values = cur.fetchall()

        if not values:

            sql = ''' INSERT INTO table_fscrawler(fpath,fdigest,fmtime,rectime) VALUES(?,?,?,?)'''
            task = (path_filenames[i],digests[i],modified_time[i],datetime_obj)
            cur.execute(sql, task)
            conn.commit()
            print('Attention! A new file has been added, Please refer database for more information')
        else:
            values = str(values[0][0])

            if digests[i]!=values:

                sql = ''' INSERT INTO table_fscrawler(fpath,fdigest,fmtime,rectime) VALUES(?,?,?,?)'''
                task = (path_filenames[i],digests[i],modified_time[i],datetime_obj)
                cur.execute(sql, task)
                conn.commit()
                print("One or more has been changed, Please refer database for more information")
        current_path = []

'''Crating connection to the database'''
def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Exception as e:
        print(e)


'''main function makes a call to file_crawler'''
if __name__ == "__main__":
    database = 'fscrawler'
    conn = create_connection(database)
    try:
        x = sys.argv[1]
        y = sys.argv[2]
    except:
        print("\nError: missing parameters Usage:  myprogram <path_to_scan> <full|top>\n\n<path_to_scan> - a valid directory path to be scanned for file changes \n<full|top> - full: performs recursive scanning; top: scans the top directory only")
    else:
       file_crawler(x,y,conn)
