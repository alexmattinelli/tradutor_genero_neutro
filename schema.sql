CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original TEXT NOT NULL,
    traducao TEXT NOT NULL,
    correto BOOLEAN NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vocabulario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palavra_masc TEXT NOT NULL,
    palavra_neutra TEXT NOT NULL,
    exemplos TEXT
);

INSERT OR IGNORE INTO vocabulario (palavra_masc, palavra_neutra) VALUES
    ('o', 'ê'),
    ('a', 'ê'),
    ('menino', 'menine'),
    ('menina', 'menine'),
    ('todos', 'todes'),
    ('todas', 'todes');