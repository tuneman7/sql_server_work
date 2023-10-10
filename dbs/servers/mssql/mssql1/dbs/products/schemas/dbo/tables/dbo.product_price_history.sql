use products;
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[product_price_history]') AND type in (N'U'))
DROP TABLE [dbo].[product_price_history]
go
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[product_price_history](
	[id] [int] IDENTITY(1,1) PRIMARY KEY,
	product_id int not null,
	usd_price money not null,
	[pricing_start_dt] [datetime] not NULL,
	[pricing_end_dt] [datetime] not NULL,
	[created_by] [char](100) NULL DEFAULT system_user,
	[created_dt] [datetime] NULL default getdate(),
	[updated_by] [char](100) NULL,
	[updated_dt] [datetime] NULL
) ON [PRIMARY]
GO
ALTER TABLE product_price_history
ADD CONSTRAINT FK_product_price_history_product
FOREIGN KEY (product_id)
REFERENCES products(id);
go
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- Create the trigger to update updated_dt
CREATE TRIGGER [dbo].[Updateproduct_price_history]
ON [dbo].[product_price_history]
AFTER UPDATE
AS
BEGIN
    UPDATE product_price_history
    SET updated_dt = GETDATE(),
	updated_by = system_user
    FROM product_price_history
    INNER JOIN inserted ON product_price_history.id = inserted.id;
END;
GO
ALTER TABLE [dbo].[product_price_history] ENABLE TRIGGER [Updateproduct_price_history]
GO
