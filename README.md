# BabyNames
# Tables

# summaryTables.sqlite contains four tables

<!-- stateGender is for the chloropleth visualizations -->
CREATE TABLE "stateGender" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"State"	TEXT,
	"Year"	INTEGER,
	"Gender"	TEXT,
	"total_count"	INTEGER
)

<!-- top50 is for the word cloud visulization -->
CREATE TABLE "top50" (
	"Name"	TEXT,
	"total_count"	INTEGER,
	PRIMARY KEY("Name")
)

<!-- year name is for the line chart visulizations -->
CREATE TABLE "yearName" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT,
	"Year"	INTEGER,
	"total_count"	INTEGER
)

<!-- NameYearCount was going to be used but the data visulizes poorly  -->
CREATE TABLE "NameYearCount" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT,
	"yearCount"	INTEGER
)
