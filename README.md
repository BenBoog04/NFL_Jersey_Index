# CSE 412 Assignment 04 – NFL Jersey Sale Index Project

## Prereqs
- PostgreSQL -> installed
- Python 3.8+ -> conda/pip
    -> pip install Flask
    -> pip install psycopg2-binary


## Backend only (no separate front-end project):

- No Node.js required
- No npm required

## Back-end Setup
### 1. Extract the ZIP (provided for grading)

Unzip the submission folder.
Inside you will see:

app.py
schema.sql
database/
    orders.csv
    jersey_sales.csv
    data_generation.py
templates/
    index.html

### 2. Create PostgreSQL Database

Open pgAdmin
In the Query Tool, run:

CREATE DATABASE nfl_jersey_db;

### 3. Activate a Virtual Environment (recommended)

In the project root folder:

python3 -m venv .venv
source .venv/bin/activate

### 4. Install Dependencies

Run:

pip install Flask
pip install psycopg2-binary

### 5. Set Up Database Schema

Run the schema file:

psql -U postgres -d nfl_jersey_db -f schema.sql

### 6. Configure Data Generation Script

Open database/data_generation.py and update:

DB_CONFIG = {
    'dbname': 'nfl_jersey_db',
    'user': 'postgres',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}

### 7. Populate Database with 10,000+ Tuples

In the project root:

python database/data_generation.py


This loads both CSV files into the two tables:

orders

jersey_sales

### 8. Configure Flask Backend

Open app.py and update the DB settings:

DB_CONFIG = {
    'dbname': 'nfl_jersey_db',
    'user': 'postgres',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}

### 9. Run Flask Backend

In the root folder:

python app.py


Your server will start at:

http://localhost:5000

## Using the Application

### 1. Open the Web Interface

Navigate to:

http://localhost:5000


You will see the simplified UI containing:

Search Without Indexing

Search Option 01: Single-table query (jersey_sales)

Search Option 02: Joined query (orders + jersey_sales)

Search With Indexing

Same two queries, but with indexes created beforehand

### 2. How to Perform Searches

Enter full player name (example: Patrick Mahomes)

Enter state as full name or abbreviation (California or CA)

Click search under:

“Single Table Search”

“Two Table Search”

Each search displays:

Query execution time (in ms)

Top 5 results in a table

Clear separation between indexed and unindexed performance

### 3. Viewing Index Impact

To meet assignment requirements :

Each query runs twice (with and without indexes)

Execution times are measured using Python timers

Index mode automatically adds:

CREATE INDEX idx_player_name ON jersey_sales(jerseyname);
CREATE INDEX idx_state ON orders(shippingstate);