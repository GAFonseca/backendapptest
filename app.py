from flask import Flask, jsonify, make_response
from collections import defaultdict
import csv
import sqlite3
from markupsafe import escape

# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set(style="whitegrid",rc={"figure.figsize": (17, 8)})

app = Flask(__name__)

DATABASE = 'database.db'
appHasRunBefore:bool = False



def create_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (year INTEGER, title TEXT, studios TEXT, producer TEXT, winner TEXT)''')
    conn.commit()
    conn.close()


def insert_data_from_csv():
    conn = sqlite3.connect(DATABASE)

    try:
        with open('data/movielist.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            # Check if the CSV file has the expected columns
            if not all(key in reader.fieldnames for key in ['year', 'title', 'studios', 'producers', 'winner']):
                raise FileNotFoundError("CSV file doesn't follow the expected schema")

            rows = [(int(row['year']), row['title'], row['studios'], row['producers'], row['winner']) for row in reader]

            c = conn.cursor()
            c.executemany('INSERT INTO movies VALUES (?, ?, ?, ?, ?)', rows)
            conn.commit()
            conn.close()
    except FileNotFoundError as e:
        # Rollback the changes if the CSV file doesn't follow the expected schema
        conn.rollback()
        raise e

@app.before_request
def before_first_request():

    global appHasRunBefore
    if not appHasRunBefore:
        create_database()
        insert_data_from_csv()
        appHasRunBefore=True




@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Endpoint not found'}), 404)

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
    max_interval = float('-inf')
    min_interval = float('inf')
    for producer, intervals in producers.items():
        interval = min(intervals, key=lambda x: x["interval"])
        if interval["interval"]<min_interval:
            min_interval = interval["interval"]
            results_min = [interval]
        elif interval["interval"]==min_interval:
            results_min.append(interval)

        interval = max(intervals, key=lambda x: x["interval"])
        if interval["interval"]>max_interval:
            max_interval = interval["interval"]
            results_max = [interval]
        elif interval["interval"]==max_interval:
            results_max.append(interval)

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