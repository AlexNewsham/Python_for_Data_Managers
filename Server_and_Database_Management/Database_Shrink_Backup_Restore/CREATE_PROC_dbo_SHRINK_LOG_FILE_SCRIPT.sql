USE [Util]
GO

/****** Object:  StoredProcedure [dbo].[SHRINK_LOG_FILE]    Script Date: 24/06/2024 14:23:41 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


/*
** CREATED BY: ALEX NEWSHAM
** CREATED ON: 13/06/2024
** PURPOSE:    TO AUTOMATE THE SHRINKAGE OF LOG FILES FOR A SPECIFIED DATABASE
**
*/
create procedure [dbo].[SHRINK_LOG_FILE]
@DBNAME SYSNAME 
AS

/*
-- N.B. (1) RUN COMMANDS IN THE TRANSACTION AS SEPARATE COMMANDS (I.E. USING SEMI-COLON) TO AVOID USING "GO" AS USING "GO" RESULTS IN AN ERROR (BECAUSE GO IS NOT A TSQL COMMAND BUT 
--          A MANAGEMENT STUDIO COMMAND AND THEREFORE NOT IN THE SCOPE OF DYNAMIC SQL)
--      (2) USE QUOTENAME() FUNCTION TO SQL INJECTION BY WRAPPING DBNAME IN SQUARE BRACKETS
*/

DECLARE @sql_trans NVARCHAR(MAX)

SET @sql_trans = N'USE ' + QUOTENAME(@DBNAME) + ';

SELECT file_id, type_desc,
       CAST(FILEPROPERTY(name, ''SpaceUsed'') AS decimal(19,4)) * 8 / 1024. AS space_used_mb,
       CAST(size/128.0 - CAST(FILEPROPERTY(name, ''SpaceUsed'') AS int)/128.0 AS decimal(19,4)) AS space_unused_mb,
       CAST(size AS decimal(19,4)) * 8 / 1024. AS space_allocated_mb,
       CAST(max_size AS decimal(19,4)) * 8 / 1024. AS max_size_mb
FROM sys.database_files;

ALTER DATABASE ' + QUOTENAME(@DBNAME) + '
SET RECOVERY SIMPLE;

-- Shrink the truncated log file to 1 MB.
DBCC SHRINKFILE (' + QUOTENAME(@DBNAME) +', 1);

ALTER DATABASE ' + QUOTENAME(@DBNAME) + '
SET RECOVERY FULL;

SELECT file_id, type_desc,
       CAST(FILEPROPERTY(name, ''SpaceUsed'') AS decimal(19,4)) * 8 / 1024. AS space_used_mb,
       CAST(size/128.0 - CAST(FILEPROPERTY(name, ''SpaceUsed'') AS int)/128.0 AS decimal(19,4)) AS space_unused_mb,
       CAST(size AS decimal(19,4)) * 8 / 1024. AS space_allocated_mb,
       CAST(max_size AS decimal(19,4)) * 8 / 1024. AS max_size_mb
FROM sys.database_files; ';

PRINT (@sql_trans);
EXECUTE (@sql_trans);
GO


