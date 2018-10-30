# Facebook-Watchman-Prototype

Purpose

  Scan particular filesystem directory or directories. Tracks the files changes using a digest sum and last modification time. Stores the information in a database table. Provides a search utility to find all modified files for particular time range.
 
Specification
  
Standalone multithreaded allocation. Java or Python.
The JDBC URL, the directories, the scan interval and whatever else required shall be provided in a configuration file.
UI or command line interface for search capabilities.




To run file_crawler_v3.py run the following command:

               Python file_crawler_v3.py  path  type(full/top)
 
To run main_program.py run the following command:
   
              Python main_program.py  startdate  enddate  filepath(optional)
 
Method:

a)	This project is divided into two modules. First module(file_crawler_v3.py) runs in the background and updates the database after every n scan-interval. Second module is a search functionality(main_program.py) that searches the database based on time inputs by user as shown in the screenshot.

b)	file_crawler_v3.py(file crawler version 3): This script runs in the background and take parameters from crontab and updates the database if any changes occur in the existing files(hash value changes) or Insert the data whenever new file is created. 

c)	Crontab: Crontab is used to schedule the script by passing required arguments needed for the script to run. 
d)	To create a crontab file run the following command on your command line:

    export EDITOR=vim; crontab -e
              This command will open the vim editor and there you can specify time and parameters to  schedule the job as shown below
                       
    */20 */6 * * * python /home/i871175/file_crawler_v3.py /home/i871175/prasunproject full
 
    */20 * * * * python /home/i871175/file_crawler_v3.py /home/i871175/ top
 
The first command runs the script file_crawler_v3.py every 6 hours and 20 min. In this the parameters passed to the script are:-
        
        Path: /home/i871175/prasunproject      type of scan: full
 
e)	To run the main program file just type the file name followed by two inputs in the form of dates
                                    
                                    [i871175@usphlhanaags08 ~]$ python main_program.py 2018-08-18 2018-08-22
 
 
DATABASE: 
 
Schema used: 
    
    CREATE TABLE table_fscrawler(fpath varchar(2048) primary key, fdigest nvarchar(32),fmtime datetime, rectime datetime);
 
Table Name: table_fscrawler
Database Name: fscrawler

