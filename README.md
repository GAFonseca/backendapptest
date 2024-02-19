# Flask Golden Raspberry Awards Backend

This project is a simple Flask application that serves as a backend for retrieving information about Golden Raspberry Awards (Razzie Awards) nominees and winners in the category of Worst Film. It provides a RESTful API to query data about producers with the longest and shortest intervals between consecutive wins, as well as to retrieve intervals for specific producers.

## Project Directory Format

The project directory should be structured as follows:


```
project/
│
├── app.py
├── data/
│ └── movielist.csv
│
└── tests/
└── test_csv_format.p
```


- `app.py`: The main Flask application file.
- `data/`: Directory containing the CSV file with Golden Raspberry Awards data.
- `tests/`: Directory containing the integration tests for the Flask application.


## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/GAFonseca/backendapptest.git
```
2. Navigate to the project directory:

```bash
cd backendapptest
```

3. Set up a virtual environment (optional but recommended):

```bash
python -m venv venv
```
4.Activate the virtual environment:
  - On Windows:

```bash
venv\Scripts\activate
```
  - On macOS/Linux:

```bash
source venv/bin/activate
```
5. Install dependencies:
```bash
pip install -r requirements.txt
```


## Running the Application
To run the Flask application, execute the following command:

```bash
python app.py
```
The application will start running on http://localhost:5000/ by default.

##Running the Tests
To run the integration tests, execute the following command:


```bash
python -m unittest discover tests
```

This command will discover and run all the test files within the tests directory.

##API Endpoints
GET /api/producers: Retrieve minimum and maximum intervals for all producers.
GET /api/producers/<producer_name>: Retrieve minimum and maximum intervals for a specific producer.

##CSV File Format
The CSV file containing the Golden Raspberry Awards data should have the following format:


```sql
year;title;studios;producers;winner
```

## Built With

 - Flask - Web framework for Python
 - SQLite - Embedded relational database
 - unittest - Unit testing framework for Python


##License
This project is licensed under the MIT License - see the LICENSE file for details.


