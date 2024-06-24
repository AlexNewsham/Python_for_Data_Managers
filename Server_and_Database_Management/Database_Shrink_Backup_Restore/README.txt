PURPOSE: PROCESS FOR LEVERAGING PYTHON TO CLONE A SQL SERVER DATABASE FROM ONE SQL SERVER INSTANCE TO ANOTHER

First, use the following SQL scripts bundled in this project to create SQL Server databases and procedures, which are called by the Python script ('clone_database_from_one_server_to_another.py'): 

- "CREATE_Util_DATABASE_SCRIPT.sql" to create a database called Util on both you source and destination instances of SQL Server. These will store your SQL procedures to be used with the Python CLONE script

- "CREATE_PROC_dbo_BACKUP_TO_DEVICE_Script.sql" to create the shrink log file procedure on the your source SQL server instance of the Util database
- "" to create the back up to device procedure on the your source SQL server instance of the Util database
- "CREATE_PROC_dbo_RestoreDatabase_SCRIPT.sql" to create the database restore procedure on your destination SQL server instance of the Util database


Finally, amend the following Python script as prompted setting the variables with source and destination database names, filepaths and directories:

	clone_database_from_one_server_to_another.py

You can then run this script to run the entire procees. 

N.B. To mitigate error, I strongly advise you run this script against a development/test instance(s) of SQL Server befor using the script against production servers.