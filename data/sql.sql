CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, 
  hash TEXT NOT NULL, 
  email TEXT NOT NULL, 
  grp_id INTEGER
  );

CREATE UNIQUE INDEX username 
ON users (username);

-- INSERT INTO users (username, hash, email) 
-- VALUES ("Nikola", "hushhush123", "nikolav@yahoo.com");

CREATE TABLE groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, grp_number INTEGER NOT NULL, 
  grp_class TEXT NOT NULL
  );

CREATE UNIQUE INDEX grp_number 
ON groups (grp_number);

DROP TABLE groups;

CREATE TABLE kids (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
  name TEXT NOT NULL, 
  hash TEXT NOT NULL,  
  grp_id INTEGER NOT NULL,
  grp_number INTEGER NOT NULL
  );

CREATE UNIQUE INDEX username 
ON users (username);

CREATE TABLE chores (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  chore TEXT NOT NULL, 
  group_id INTEGER NOT NULL
  );

CREATE TABLE chores (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  chore TEXT NOT NULL, 
  group_id INTEGER NOT NULL
  );