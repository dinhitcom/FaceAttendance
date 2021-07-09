IF OBJECT_ID(N'[__EFMigrationsHistory]') IS NULL
BEGIN
    CREATE TABLE [__EFMigrationsHistory] (
        [MigrationId] nvarchar(150) NOT NULL,
        [ProductVersion] nvarchar(32) NOT NULL,
        CONSTRAINT [PK___EFMigrationsHistory] PRIMARY KEY ([MigrationId])
    );
END;
GO

BEGIN TRANSACTION;
GO

CREATE TABLE [Students] (
    [StudentID] nvarchar(450) NOT NULL,
    [Fullname] nvarchar(max) NOT NULL,
    [Class] nvarchar(max) NULL,
    [Email] nvarchar(max) NULL,
    CONSTRAINT [PK_Students] PRIMARY KEY ([StudentID])
);
GO

CREATE TABLE [Teachers] (
    [TeacherID] int NOT NULL IDENTITY,
    [Fullname] nvarchar(max) NOT NULL,
    [Email] nvarchar(max) NOT NULL,
    [Password] nvarchar(max) NOT NULL,
    CONSTRAINT [PK_Teachers] PRIMARY KEY ([TeacherID])
);
GO

CREATE TABLE [StudentImages] (
    [ImageID] nvarchar(450) NOT NULL,
    [StudentID] nvarchar(450) NOT NULL,
    [EncodeImage] nvarchar(max) NULL,
    CONSTRAINT [PK_StudentImages] PRIMARY KEY ([ImageID]),
    CONSTRAINT [FK_StudentImages_Students_StudentID] FOREIGN KEY ([StudentID]) REFERENCES [Students] ([StudentID]) ON DELETE CASCADE
);
GO

CREATE TABLE [Classes] (
    [ClassID] nvarchar(450) NOT NULL,
    [Class_Name] nvarchar(max) NOT NULL,
    [TeacherID] int NOT NULL,
    [ClassTime] int NOT NULL,
    CONSTRAINT [PK_Classes] PRIMARY KEY ([ClassID]),
    CONSTRAINT [FK_Classes_Teachers_TeacherID] FOREIGN KEY ([TeacherID]) REFERENCES [Teachers] ([TeacherID]) ON DELETE CASCADE
);
GO

CREATE TABLE [Attendances] (
    [AttendanceID] nvarchar(450) NOT NULL,
    [StudentID] nvarchar(450) NOT NULL,
    [ClassID] nvarchar(450) NOT NULL,
    [AttendanceDate] datetime2 NOT NULL,
    [AttendanceTime] datetime2 NOT NULL,
    CONSTRAINT [PK_Attendances] PRIMARY KEY ([AttendanceID]),
    CONSTRAINT [FK_Attendances_Classes_ClassID] FOREIGN KEY ([ClassID]) REFERENCES [Classes] ([ClassID]) ON DELETE CASCADE,
    CONSTRAINT [FK_Attendances_Students_StudentID] FOREIGN KEY ([StudentID]) REFERENCES [Students] ([StudentID]) ON DELETE CASCADE
);
GO

CREATE TABLE [StudentClass] (
    [StudentID] nvarchar(450) NOT NULL,
    [ClassID] nvarchar(450) NOT NULL,
    CONSTRAINT [PK_StudentClass] PRIMARY KEY ([StudentID], [ClassID]),
    CONSTRAINT [FK_StudentClass_Classes_ClassID] FOREIGN KEY ([ClassID]) REFERENCES [Classes] ([ClassID]) ON DELETE CASCADE,
    CONSTRAINT [FK_StudentClass_Students_StudentID] FOREIGN KEY ([StudentID]) REFERENCES [Students] ([StudentID]) ON DELETE CASCADE
);
GO

CREATE INDEX [IX_Attendances_ClassID] ON [Attendances] ([ClassID]);
GO

CREATE INDEX [IX_Attendances_StudentID] ON [Attendances] ([StudentID]);
GO

CREATE INDEX [IX_Classes_TeacherID] ON [Classes] ([TeacherID]);
GO

CREATE INDEX [IX_StudentClass_ClassID] ON [StudentClass] ([ClassID]);
GO

CREATE INDEX [IX_StudentImages_StudentID] ON [StudentImages] ([StudentID]);
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709053845_InitialCreate', N'5.0.6');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

ALTER TABLE [Attendances] DROP CONSTRAINT [FK_Attendances_Classes_ClassID];
GO

ALTER TABLE [Attendances] DROP CONSTRAINT [FK_Attendances_Students_StudentID];
GO

DROP INDEX [IX_Attendances_ClassID] ON [Attendances];
GO

DROP INDEX [IX_Attendances_StudentID] ON [Attendances];
GO

ALTER TABLE [StudentClass] ADD [AbsenceTimes] int NOT NULL DEFAULT 0;
GO

DECLARE @var0 sysname;
SELECT @var0 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Attendances]') AND [c].[name] = N'StudentID');
IF @var0 IS NOT NULL EXEC(N'ALTER TABLE [Attendances] DROP CONSTRAINT [' + @var0 + '];');
ALTER TABLE [Attendances] ALTER COLUMN [StudentID] nvarchar(max) NOT NULL;
GO

DECLARE @var1 sysname;
SELECT @var1 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Attendances]') AND [c].[name] = N'ClassID');
IF @var1 IS NOT NULL EXEC(N'ALTER TABLE [Attendances] DROP CONSTRAINT [' + @var1 + '];');
ALTER TABLE [Attendances] ALTER COLUMN [ClassID] nvarchar(max) NOT NULL;
GO

ALTER TABLE [Attendances] ADD [StudentClassClassID] nvarchar(450) NULL;
GO

ALTER TABLE [Attendances] ADD [StudentClassStudentID] nvarchar(450) NULL;
GO

CREATE INDEX [IX_Attendances_StudentClassStudentID_StudentClassClassID] ON [Attendances] ([StudentClassStudentID], [StudentClassClassID]);
GO

ALTER TABLE [Attendances] ADD CONSTRAINT [FK_Attendances_StudentClass_StudentClassStudentID_StudentClassClassID] FOREIGN KEY ([StudentClassStudentID], [StudentClassClassID]) REFERENCES [StudentClass] ([StudentID], [ClassID]) ON DELETE NO ACTION;
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709060139_UpdateModel', N'5.0.6');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

DECLARE @var2 sysname;
SELECT @var2 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Attendances]') AND [c].[name] = N'ClassID');
IF @var2 IS NOT NULL EXEC(N'ALTER TABLE [Attendances] DROP CONSTRAINT [' + @var2 + '];');
ALTER TABLE [Attendances] DROP COLUMN [ClassID];
GO

DECLARE @var3 sysname;
SELECT @var3 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Attendances]') AND [c].[name] = N'StudentID');
IF @var3 IS NOT NULL EXEC(N'ALTER TABLE [Attendances] DROP CONSTRAINT [' + @var3 + '];');
ALTER TABLE [Attendances] DROP COLUMN [StudentID];
GO

EXEC sp_rename N'[Classes].[Class_Name]', N'ClassName', N'COLUMN';
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709061003_UpdateDatabase', N'5.0.6');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

DECLARE @var4 sysname;
SELECT @var4 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Classes]') AND [c].[name] = N'ClassTime');
IF @var4 IS NOT NULL EXEC(N'ALTER TABLE [Classes] DROP CONSTRAINT [' + @var4 + '];');
ALTER TABLE [Classes] ALTER COLUMN [ClassTime] nvarchar(max) NULL;
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709095504_UpdateClass', N'5.0.6');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

DECLARE @var5 sysname;
SELECT @var5 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[StudentClass]') AND [c].[name] = N'AbsenceTimes');
IF @var5 IS NOT NULL EXEC(N'ALTER TABLE [StudentClass] DROP CONSTRAINT [' + @var5 + '];');
ALTER TABLE [StudentClass] DROP COLUMN [AbsenceTimes];
GO

ALTER TABLE [Students] ADD [AbsenceTimes] int NOT NULL DEFAULT 0;
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709105701_UpdateStudent', N'5.0.6');
GO

COMMIT;
GO

BEGIN TRANSACTION;
GO

DECLARE @var6 sysname;
SELECT @var6 = [d].[name]
FROM [sys].[default_constraints] [d]
INNER JOIN [sys].[columns] [c] ON [d].[parent_column_id] = [c].[column_id] AND [d].[parent_object_id] = [c].[object_id]
WHERE ([d].[parent_object_id] = OBJECT_ID(N'[Students]') AND [c].[name] = N'AbsenceTimes');
IF @var6 IS NOT NULL EXEC(N'ALTER TABLE [Students] DROP CONSTRAINT [' + @var6 + '];');
ALTER TABLE [Students] DROP COLUMN [AbsenceTimes];
GO

ALTER TABLE [StudentClass] ADD [AbsenceTimes] int NOT NULL DEFAULT 0;
GO

INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
VALUES (N'20210709120957_Revert', N'5.0.6');
GO

COMMIT;
GO

