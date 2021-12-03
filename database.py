import os
import sqlite3 as sql

# change path to desired location
path = os.path.join('saves', 'highscores.db')


def create_database():
    con = sql.connect(path)
    # only creates the table if it does not already exist.
    con.execute('CREATE TABLE IF NOT EXISTS Stats (Kill_Count INTEGER, Level INTEGER, Game_Time FLOAT)')
    con.close()


def save_scores(kill_count, level, game_time):
    # safe call to create since table check is in place
    create_database()
    try:
        # connect to database
        with sql.connect(path) as con:
            cur = con.cursor()

            # Insert scores into db table
            cur.execute(
                'INSERT INTO Stats (Kill_Count, Level, Game_Time) VALUES (?,?,?)',
                (kill_count, level, game_time))

            # commit changes
            con.commit()
    except:
        # rollback if any errors.
        con.rollback()

    finally:
        # close db connection
        con.close()


def load_scores():
    # safe call to create since table check is in place
    create_database()
    con = sql.connect(path)
    con.row_factory = sql.Row

    cur = con.cursor()

    cur.execute('SELECT Kill_Count, Level, Game_Time FROM Stats ORDER BY Game_Time ASC, Kill_Count LIMIT 10')

    # Get all rows of scores (as tuples) and store in list
    scoreList = cur.fetchall()

    # return top ten scores (tuples) in order of kill count
    return scoreList
