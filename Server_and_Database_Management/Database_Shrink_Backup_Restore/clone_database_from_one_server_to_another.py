import os
from datetime import datetime
import shutil
import pyodbc
import textwrap

##########################################################################################################################
#author: Alex Newsham
#date:   14/06/2024
#purpose: To facilitate database cloning from one server to another, changing the database name on the destination server
#
#notes: (1) Remember to set variables and substitute in your database, server and filepath references
#       (2) Remember to build the stored procedures referenced in this script for which the create statements have been 
#           provided in this repo: [dbo].[SHRINK_LOG_FILE] are [dbo].[BACKUP_TO_DEVICE] are needed on the source server; 
#           [dbo].[RestoreDatabase] is needed on the destination server. Use the database creation script provided to 
#           create the Util database on both your source and destination folder. 
#
#########################################################################################################################

database_name = '' #Add the SOURCE database to back up e.g. 'MyDatabase'
backup_path = '' #Add the mapped FILEPATH of the backup device on SOURCE SQL Server Machine as readable by SQL e.g., 'G:/TempBackup/mydatabase.bak' as the local file path
restore_backup_device_fp = '' #Add the file path of the backup file on destination SQL Server machine
target_database_name = '' #Add the estination database name e.g. 'MyDatabase'

BackupDeviceFP1 = '' #Add the full backup FILEPATH on SOURCE server for remote access e.g., '//MYServer/G$/TempBackup/MyDatabase.bak'
BackupDeviceFP2 = '' #Add the full backup FILEPATH on the DESTINATION server for remote access e.g., //MyServer/G$/Program Files/Microsoft SQL Server/MSSQL16.MSSQLSERVER/MSSQL/Backup/TempAdhocBackup/MyDatabase.bak'
BackupDir_1 = '' #Add the full backup DIRECTORY on SOURCE server for remote access e.g., '//MYServer/G$/TempBackup'
BackupDir_2 = '' #Add the full backup DIRECTORY on the DESTINATION server for remote access e.g., '//MyServer/G$/Program Files/Microsoft SQL Server/MSSQL16.MSSQLSERVER/MSSQL/Backup/TempAdhocBackup/'

# connections - add 'autocommit = True' to prevent the error: '[42000] [Microsoft][ODBC SQL Server Driver][SQL Server]Cannot perform a backup or restore operation within a transaction.' 
conn1 = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=MyServer;Database=Util;Trusted_Connection=Yes;', autocommit=True)
conn2 = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=MyServer;Database=tempdb;Trusted_Connection=Yes;', autocommit=True)
conn3 = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=MyServer;Database=Util;Trusted_Connection=Yes;', autocommit=True)


# shrink database's log file
print(str("Shrink database log file before backup..."))
spShrinkExec = "EXECUTE [dbo].[SHRINK_LOG_FILE] @DBNAME=?"
conn1.execute(spShrinkExec, database_name)
conn1.commit()

# run backup to device procedure 
print(str("Initiating database backup to device file..."))
strSQLBackup = textwrap.dedent(
    f"""
        DECLARE	@return_value int
        EXEC	@return_value = [dbo].[BACKUP_TO_DEVICE]
		        @DbName = N'{database_name}',
		        @BackUpDeviceFilePath = N'{backup_path}'
    
    """
    )
print(str(strSQLBackup))
cursor1 = conn1.cursor()  #set the cursor connection
cursor1.execute(strSQLBackup)
while cursor1.nextset():  #Pyodbc won't progress past info messages automatically, so this while loop ensures it loops through the messages before closing the cursor.
    pass 
cursor1.close()
conn1.close()

# if back up device file exists in destination folder the remove it
print(str("IF EXISTS, Remove backup device file from destination backup folder..."))
try:
    os.remove(BackupDeviceFP2)
except OSError:
    pass

# move backup device file from temp backup folder on dv server to res 22a server temp backup fol
print(str("Move backup file to new backup folder destination..."))
shutil.move(BackupDeviceFP1,BackupDir_2)

#drop copy of EpiVault database if exists
print(str("Initiating drop database..."))
sqlStrDrop = textwrap.dedent(
    f"""
        IF EXISTS (SELECT 1 FROM sys.databases WHERE [name] = '{target_database_name}')
        BEGIN
            ALTER DATABASE [{target_database_name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
            USE [tempdb];
            DROP DATABASE [{target_database_name}];
        END;    
    """
)

#print string, set new cursor then and execute sql command string then close cursor and connection
print(str(sqlStrDrop))
cursor2 = conn2.cursor()
cursor2.execute(sqlStrDrop)
cursor2.close()
conn2.close()


#restore latest backup of database 
print(str("Initiating Database Restore from backup device..."))
sqlStrRestore =textwrap.dedent(
    f"""
        DECLARE	@return_value int
        EXEC	@return_value = [dbo].[RestoreDatabase]
		@backupDeviceFilePath = N'{restore_backup_device_fp}',
		@destinationDatabaseName = {target_database_name}      
    """
    )
print(str(sqlStrRestore))
cursor3 = conn3.cursor()
cursor3.execute(sqlStrRestore)
while cursor3.nextset():  #Pyodbc won't progress past info messages automatically, and RESTORE generates a lot of them. So you must process them with cursor.nextset() otherwise Restore will abort without completing.
    pass 
cursor3.close()
conn3.close()

#Finally remove the backup device from the temp folder on the destination server
# if back up device file exists in destination folder the remove it
print(str("Finally, clean up and remove back up device from destination server backup folder..."))
try:
    os.remove(BackupDeviceFP2)
except OSError:
    pass

print(str("End of script!"))




