USE [Util]
GO

/****** Object:  StoredProcedure [dbo].[BACKUP_TO_DEVICE]    Script Date: 24/06/2024 14:22:23 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




/*
** Created by: Alex Newsham
** Created on: 14/06/2024
** Purpose: To facilitate ad hoc backups to a device that can be used for downstream purposes - e.g. cloning of a database on a different server
*/
CREATE procedure [dbo].[BACKUP_TO_DEVICE]
@DbName SYSNAME null,
@BackUpDeviceFilePath varchar(500) null
as
begin
	declare @sql_trans NVARCHAR(MAX), @Success varchar(200);

	set @sql_trans = N'BACKUP DATABASE ' + QUOTENAME(@DBNAME) + ' 
	TO DISK = ''' + @BackUpDeviceFilePath +'''
	   WITH FORMAT,
		  MEDIANAME = ''SQLServerBackups'',
		  NAME = ''Full Backup of ' + @DbName + ''';';

	set @Success = 'Process completed'

	SELECT @Success as ProcessResult
	
	PRINT(@sql_trans);
	EXECUTE(@sql_trans);

	RETURN
	
end
GO


