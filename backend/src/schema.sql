CREATE TABLE IF NOT EXISTS "user"
(
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NULL,
    password VARCHAR(50)        NULL
);

CREATE TABLE IF NOT EXISTS movie
(
    id     SERIAL PRIMARY KEY,
    title  TEXT NOT NULL,
    genres TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rating
(
    rating    REAL NOT NULL,
    timestamp TIMESTAMP   NOT NULL,
    movieId   INT,
    userId    INT,
    CONSTRAINT fkMovie
        FOREIGN KEY (movieId) REFERENCES movie (id),
    CONSTRAINT fkUser
        FOREIGN KEY (userId) REFERENCES "user" (id),
    PRIMARY KEY (movieId, userId)
);