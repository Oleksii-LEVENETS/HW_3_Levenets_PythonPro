import sqlite3

from flask import (
    Blueprint, render_template, current_app
)

bp = Blueprint('music', __name__, url_prefix='/music')


# 1. Вью функция должна выводить количество уникальных исполнителей (artist) из таблицы tracks.
# PATH: /names/
@bp.route('/names/')
def names():
    db = sqlite3.connect(current_app.config['DATABASE'])
    num_uniq = len(set(db.execute('SELECT artist FROM tracks').fetchall()))
    return render_template("render_file.html", filename='/names/',
                           content=f'Kоличество уникальных artist из таблицы tracks: {num_uniq}')


# 2. Вью функция должна выводить количество записей из таблицы tracks.
# PATH: /tracks/
@bp.route('/tracks/')
def tracks():
    db = sqlite3.connect(current_app.config['DATABASE'])
    num_tracks = db.execute('SELECT COUNT (id) FROM tracks').fetchone()[0]
    return render_template("render_file.html", filename='/tracks/',
                           content=f'Kоличество записей из таблицы tracks: {num_tracks}')


# 3. Вью функция должна принимать название жанра трека и выводить количество записей этого жанра (genre) из tracks.
# PATH: /tracks/<genre>
@bp.route('/tracks_genre/')
def tracks_genre():
    db = sqlite3.connect(current_app.config['DATABASE'])
    genre_l = db.execute('SELECT title FROM genres').fetchall()
    return render_template("2_3_genre_num_track.html", filename='/tracks_genre/', content=genre_l)


@bp.route('/tracks/<genre>')
def count_genre(genre):
    db = sqlite3.connect(current_app.config['DATABASE'])
    count_g = db.execute('SELECT COUNT (tracks.id) '
                         ' FROM tracks JOIN genres ON tracks.genre_id = genres.id'
                         ' WHERE genres.title = ?',
                         (genre.capitalize(),)
                         ).fetchone()[0]
    
    return render_template("render_file.html", filename=f'/tracks/{genre}',
                           content=f'Kоличество записей жанра {genre.capitalize()} из tracks: {count_g}')


# 4. Вью функция должна выводить все названия треков (title) и соответствующую продолжительность трека
# в секундах(length) из таблицы tracks.  PATH: /tracks-sec/
@bp.route('/tracks-sec/')
def tracks_sec():
    db = sqlite3.connect(current_app.config['DATABASE'])
    tracks_s = db.execute('SELECT title, length  FROM tracks').fetchall()
    return render_template("2_4_track_sec.html", filename='/tracks-sec/', content=tracks_s)


# 5. Вью функция должна выводить среднюю продолжительность трека и общую продолжительность всех треков в секундах
# из таблицы tracks. PATH: /tracks-sec/statistics/
@bp.route('/tracks-sec/statistics/')
def tracks_sec_stat():
    db = sqlite3.connect(current_app.config['DATABASE'])
    tracks_s_stat = db.execute('SELECT AVG(length), SUM(length) FROM tracks').fetchone()
    return(f"Cредняя продолжительность трека {tracks_s_stat[0]} секунд"
           f" и общая продолжительность всех треков {tracks_s_stat[1]} в секундах из таблицы tracks")
