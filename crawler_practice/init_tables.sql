CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    page INTEGER,
    title TEXT,
    subtitle TEXT,
    written TEXT,
    modified TEXT,
    writer TEXT,
    extra TEXT
);
