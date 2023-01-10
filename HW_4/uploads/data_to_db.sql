INSERT INTO
    tracks (
        id, title, artist, genre_id, length
    )
VALUES
    (1, 'Song_1', 'Artist_1', 1, 60),
    (2, 'Song_2', 'Artist_2', 2, 70),
    (3, 'Song_3', 'Artist_3', 3, 80),
    (4, 'Song_4', 'Artist_4', 4, 90),
    (5, 'Song_5', 'Artist_1', 1, 100),
    (6, 'Song_6', 'Artist_2', 2, 110),
    (7, 'Song_7', 'Artist_3', 3, 120),
    (8, 'Song_8', 'Artist_1', 1, 130),
    (9, 'Song_9', 'Artist_2', 1, 140),
    (10, 'Song_1', 'Artist_2', 1, 60);

INSERT INTO
    genres (
        id, title
    )
VALUES
    (1, 'Pop'),
    (2, 'Rock'),
    (3, 'Chill'),
    (4, 'Folk');
