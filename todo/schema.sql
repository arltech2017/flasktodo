PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NUll, 
    date TEXT NOT NULL,
    description TEXT,
    done BOOLEAN
);
COMMIT;
