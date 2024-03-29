CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    confirmed INTEGER DEFAULT 0,
    name TEXT,
    bid TEXT
);

CREATE TABLE token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    token TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
        ON DELETE CASCADE
);

CREATE TABLE chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    name TEXT
);

CREATE TABLE membership (
    user_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
        ON DELETE CASCADE,
    FOREIGN KEY(chat_id) REFERENCES chat(id)
        ON DELETE CASCADE
);

CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time TEXT NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY(chat_id) REFERENCES chat(id)
        ON DELETE CASCADE
);
