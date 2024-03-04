# db_utils.py

import psycopg2
import pytz
from datetime import datetime


def connect_to_database():
    """Create and return a database connection."""
    conn = None
    try:
        # Update these parameters to fit your database connection details
        conn = psycopg2.connect(
            dbname="autolab",
            user="yacine",  # database user
            password="",  # database password
            host="localhost"  # database host
         )
        return conn
    except Exception as e:\
        print(f"Failed to connect to the database: {e}")


def close_connection_to_database(conn):
    """Close the database connection."""
    try:
        if conn is not None:
            conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_driver_state_data(conn, timestamp, distraction, drowsiness):
    """Inserts driver state data into PostgreSQL database."""
    try:
        cur = conn.cursor()
        # Prepare SQL query to insert a record into the database.
        cur.execute("INSERT INTO DriverStateData (timestamp, distraction, drowsiness) VALUES (%s, %s, %s)",
                    (timestamp, distraction, drowsiness))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
