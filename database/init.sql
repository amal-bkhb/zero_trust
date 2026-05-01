CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL
);

INSERT INTO notes (content)
SELECT 'hello from database'
WHERE NOT EXISTS (SELECT 1 FROM notes);
