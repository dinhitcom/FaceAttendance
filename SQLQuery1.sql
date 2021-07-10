CREATE DATABASE StudentAttendance
GO

USE StudentAttendance
GO

CREATE TABLE Teacher (
	TeacherID int NOT NULL,
	FullName nvarchar(64) NOT NULL,
	Email varchar(256) NOT NULL UNIQUE,
	Password varchar(256) NOT NULL,
	CONSTRAINT PK_Teacher PRIMARY KEY (TeacherID)
)

CREATE TABLE Class (
	ClassID varchar(15) NOT NULL,
	ClassName nvarchar(256) NOT NULL,
	TeacherID int NOT NULL,
	ClassTime int,
	CONSTRAINT PK_Class PRIMARY KEY (ClassID),
	CONSTRAINT FK_Class_Teacher FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
)


CREATE TABLE Student(
	StudentID varchar(15) NOT NULL,
	FullName nvarchar(64) NOT NULL,
	Class nvarchar(20),
	Email varchar(256),
	CONSTRAINT PK_Student PRIMARY KEY (StudentID)
)

CREATE TABLE StudentImage (
	ImageID int NOT NULL IDENTITY(1, 1),
	StudentID varchar(15) NOT NULL,
	EncodedImage VARBINARY(MAX),
	CONSTRAINT PK_StudentImage PRIMARY KEY (ImageID),
	CONSTRAINT FK_StudentImage_Student FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
)

CREATE TABLE StudentClass(
	StudentID varchar(15) NOT NULL,
	ClassID varchar(15) NOT NULL,
	AbsenceTimes int NOT NULL,
	CONSTRAINT PK_StudentClass PRIMARY KEY (StudentID, ClassID),
	CONSTRAINT FK_StudentClass_Class FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
	CONSTRAINT FK_StudentClass_Student FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
)

CREATE TABLE Attendance(
	AttendanceID int NOT NULL IDENTITY(1, 1),
	StudentID varchar(15) NOT NULL,
	ClassID varchar(15) NOT NULL,
	AttendanceDate date,
	AttendanceTime time,
	CONSTRAINT PK_Attendance PRIMARY KEY (AttendanceID),
	CONSTRAINT FK_Attendance_StudentClass FOREIGN KEY (StudentID, ClassID) REFERENCES StudentClass(StudentID, ClassID)
)

USE StudentAttendance
GO

INSERT INTO Student VALUES 
('18IT269', N'Nguyễn Ngọc Định', '18IT5', 'nndinh.18it5@vku.udn.vn'),
('18IT351', N'Nguyễn Thị Thanh Thúy', '18IT5', 'nttthuy.18it5@vku.udn.vn'),
('BG', N'Bill Gates', 'A', 'billgates@microsoft.com'),
('ELM', N'Elon Musk', 'A', 'elonmusk@tesla.com')

INSERT INTO Teacher VALUES
(1, N'Nguyễn Văn A', 'nguyenvana@gmail.com', 'e10adc3949ba59abbe56e057f20f883e'),
(2, N'Admin', 'admin@test.com', 'e10adc3949ba59abbe56e057f20f883e'),
(3, N'Nguyễn Thị B', 'nguyenthib@gmail.com', 'e10adc3949ba59abbe56e057f20f883e'),
(4, N'Nguyễn C', 'nguyenc@gmail.com', 'e10adc3949ba59abbe56e057f20f883e')

INSERT INTO Class VALUES
('XLA1', N'Xử lý ảnh (1)', 1, 2),
('XLA2', N'Xử lý ảnh (2)', 1, 2),
('ISS3', N'Bảo mật và An toàn Hệ thống Thông tin (1)', 1, 3),
('KTPM4', N'Kiểm thử phần mềm (4)', 1, 1),
('KTPM1', N'Kiểm thử phần mềm (1)', 2, 4),
('DSP1', N'Xử lý tín hiệu số (1)', 1, 5),
('DSP2', N'Xử lý tín hiệu số (2)', 1, 5),
('ISS4', N'Bảo mật và An toàn Hệ thống Thông tin (4)', 1, 5)

INSERT INTO StudentClass VALUES 
('18IT269', 'DSP1', 0),
('ELM', 'DSP1', 0),
('BG', 'DSP1', 0),
('18IT351', 'DSP1', 0),
('18IT269', 'ISS4', 0),
('ELM', 'ISS4', 0),
('BG', 'ISS4', 0),
('18IT351', 'ISS4', 0),
('18IT269', 'XLA1', 0),
('18IT351', 'XLA1', 0),
('ELM', 'XLA1', 1),
('BG', 'XLA1', 1)

SELECT * FROM StudentClass 

INSERT INTO Attendance(StudentID, ClassID, AttendanceDate, AttendanceTime) VALUES
('18IT269', 'DSP1', '2021-07-03', '08:15:30'),
('18IT351', 'DSP1', '2021-07-03', '08:15:35'),
('ELM', 'DSP1', '2021-07-03', '08:15:40'),
('BG', 'DSP1', '2021-07-03', '08:15:45'),
('18IT269', 'XLA1', '2021-07-06', '13:15:15'),
('ELM', 'XLA1', '2021-07-06', '13:15:42'),
('BG', 'XLA1', '2021-07-06', '13:15:45') 

SELECT * FROM Attendance

SELECT ClassID, ClassName FROM Class WHERE TeacherID = 1 AND ClassTime = 5
SELECT * FROM Teacher

SELECT * FROM Class

SELECT * FROM StudentImage

curselectClass = todayClassListbox.curselection()
if curselectClass != 0:
    classId = todayClassList[curselectClass].ClassID
    print(classId)