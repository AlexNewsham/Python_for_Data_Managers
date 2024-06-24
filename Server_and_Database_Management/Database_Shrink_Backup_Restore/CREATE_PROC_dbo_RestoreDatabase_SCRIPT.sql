USE [Util]
GO

/****** Object:  StoredProcedure [dbo].[RestoreDatabase]    Script Date: 24/06/2024 14:15:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


/*
** CREATED BY: Alex Newsham
** CREATED ON: 18/06/2024
** PURPOSE: TO RESTORE A SPECIFIED DATABASE
**			STEP 1: First determine the number and names of the files in the backup. 
**			STEP 2: Run the back-up from the adhoc back up on the disk. 
**          STEP 3: Set database recovery type to "FULL"
**
**
*/

CREATE PROCEDURE [dbo].[RestoreDatabase]
@backupDeviceFilePath NVARCHAR(500) NULL, @destinationDatabaseName SYSNAME NULL
as
BEGIN
		DECLARE @sql_trans_2 NVARCHAR(MAX)

		SET @sql_trans_2 = N'
		RESTORE FILELISTONLY  
		   FROM DISK = ''' + @backupDeviceFilePath + ''';  

		RESTORE DATABASE ' + QUOTENAME(@destinationDatabaseName) + '  
		   FROM DISK = ''' + @backupDeviceFilePath + '''  
		   WITH RECOVERY;

		ALTER DATABASE ' + QUOTENAME(@destinationDatabaseName) + ' 
		SET RECOVERY FULL;'

		PRINT (@sql_trans_2);
		EXECUTE (@sql_trans_2);

END
GO


