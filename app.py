from flask import Flask, jsonify
from collections import defaultdict
import csv
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'


def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (year INTEGER, title TEXT, studios TEXT, producer TEXT, winner TEXT)''')
    conn.commit()
    conn.close()


def insert_data_from_csv():
    with open('data/movielist.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        rows = [(int(row['year']), row['title'], row['studios'], row['producers'], row['winner']) for row in reader]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.executemany('INSERT INTO movies VALUES (?, ?, ?, ?, ?)', rows)
        conn.commit()
        conn.close()


@app.before_first_request
def before_first_request():
    create_database()
    insert_data_from_csv()




@app.route('/api/producers', methods=['GET'])
def get_producer_intervals():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Query to find the intervals for each producer
    c.execute('''SELECT producer, year, winner FROM movies ORDER BY producer, year''')

    producers = defaultdict(list)
    current_producer = None
    previous_win_year = None

    for row in c.fetchall():
        producer, year, winner = row
        if winner == 'yes':
            if current_producer != producer:
                current_producer = producer
                previous_win_year = year
            else:
                interval = year - previous_win_year
                producers[producer].append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": previous_win_year,
                    "followingWin": year
                })
                previous_win_year = year

    conn.close()

    # Find the minimum and maximum intervals for each producer
    results_min = []
    results_max = []
    for producer, intervals in producers.items():
        min_interval = min(intervals, key=lambda x: x["interval"])
        max_interval = max(intervals, key=lambda x: x["interval"])
        results_min.append(min_interval)
        results_max.append(max_interval)

    return jsonify({"min": results_min, "max": results_max})


@app.route('/api/producers/<producer_name>', methods=['GET'])
def get_producer_intervals_by_name(producer_name):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Query to find the intervals for the specified producer
    c.execute('''SELECT year, winner FROM movies WHERE producer=? ORDER BY year''', (producer_name,))

    intervals = []
    previous_win_year = None

    for row in c.fetchall():
        year, winner = row
        if winner == 'yes':
            if previous_win_year:
                interval = year - previous_win_year
                intervals.append({
                    "producer": producer_name,
                    "interval": interval,
                    "previousWin": previous_win_year,
                    "followingWin": year
                })
            previous_win_year = year

    conn.close()

    # Find the minimum and maximum intervals for the producer
    if intervals:
        min_interval = min(intervals, key=lambda x: x["interval"])
        max_interval = max(intervals, key=lambda x: x["interval"])
        return jsonify({"min": min_interval, "max": max_interval})
    else:
        return jsonify({"error": "No data found for the specified producer"}), 404

if __name__ == '__main__':
    app.run(debug=True)