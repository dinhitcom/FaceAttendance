CREATE DATABASE StudentAttendance
GO

USE StudentAttendance
GO

CREATE TABLE StudentImage (
	ImageID int NOT NULL IDENTITY(1, 1),
	StudentID varchar(15) NOT NULL,
	EncodedImage VARBINARY(MAX)
)
ALTER TABLE StudentImage ADD PRIMARY KEY (ImageID)

USE StudentAttendance
GO

CREATE TABLE StudentInformation(
	StudentID varchar(15) NOT NULL,
	StudentName nvarchar(64) NOT NULL,
	Class nvarchar(20),
	Email varchar(255)
)

INSERT INTO StudentInformation VALUES 
('18IT269', N'Nguyễn Ngọc Định', '18IT5', 'nndinh.18it5@vku.udn.vn'),
('18IT351', N'Nguyễn Thị Thanh Thúy', '18IT5', 'nttthuy.18it5@vku.udn.vn'),
('BG', N'Bill Gates', 'A', 'billgates@microsoft.com'),
('ELM', N'Elon Musk', 'A', 'elonmusk@tesla.com')

SELECT * FROM StudentImage