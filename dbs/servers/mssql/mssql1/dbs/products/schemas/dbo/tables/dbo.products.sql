use products;
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[products]') AND type in (N'U'))
DROP TABLE [dbo].[products]
go
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[products](
	[id] [int] IDENTITY(1,1) PRIMARY KEY,
	[product_name] [varchar](100) NULL,
	[product_type_id] [int] NULL,
	[created_by] [char](100) NULL DEFAULT system_user,
	[created_dt] [datetime] NULL,
	[updated_by] [char](100) NULL,
	[updated_dt] [datetime] NULL,
	parent_product_id int NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[products] ADD  DEFAULT (getdate()) FOR [created_dt]
GO
ALTER TABLE products
ADD CONSTRAINT FK_ProductType
FOREIGN KEY (product_type)
REFERENCES product_type(id);
go
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- Create the trigger to update updated_dt
CREATE TRIGGER [dbo].[UpdateProducts]
ON [dbo].[products]
AFTER UPDATE
AS
BEGIN
    UPDATE products
    SET updated_dt = GETDATE(),
	updated_by = system_user
    FROM products
    INNER JOIN inserted ON products.id = inserted.id;
END;
GO
ALTER TABLE [dbo].[products] ENABLE TRIGGER [UpdateProducts]
GO
