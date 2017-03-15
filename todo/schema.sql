DROP TABLE IF EXISTS Items;
CREATE TABLE Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NUll, 
    date TEXT NOT NULL,
    decription TEXT,
    done BOOLEAN
);
