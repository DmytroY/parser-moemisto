DROP TABLE IF EXISTS dates;
DROP TABLE IF EXISTS rubrics;
DROP TABLE IF EXISTS events;

CREATE TABLE events
(
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS dates
(
    event_id INTEGER,
    date DATE,
    CONSTRAINT fk_events FOREIGN KEY (event_id) REFERENCES events (id) 
);

CREATE TABLE rubrics
(
    event_id INTEGER,
    rubric TEXT,
    CONSTRAINT fk_events FOREIGN KEY (event_id) REFERENCES events (id) 
);