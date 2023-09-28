use products;
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[product_type]') AND type in (N'U'))
DROP TABLE [dbo].[product_type]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[product_type](
	[id] [int] IDENTITY(1,1) PRIMARY KEY,
	[product_type_desc] [char](100) NULL,
	[create_dt] [datetime] default GETDATE(),
	[created_by] [char](100) default SYSTEM_USER,
	[update_dt] [datetime] NULL,
	[updated_by] [char](100) NULL
) ON [PRIMARY]
GO

-- Create a trigger on the 'product_type' table
CREATE TRIGGER tr_ProductType_Update
ON product_type
AFTER UPDATE
AS
BEGIN

    -- Update the 'update_dt' field with the current date and time
    UPDATE product_type
    SET update_dt = GETDATE(),
    updated_by = SYSTEM_USER
    FROM product_type pt
    INNER JOIN inserted i ON pt.id = i.id
END;
