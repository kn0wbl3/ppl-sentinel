import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

HOST = "localhost"  # or the IP of the container
PORT = 5432  # default PostgreSQL port
DATABASE = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

conn = None


def add_shifts_to_db(shifts):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=HOST, port=PORT, dbname=DATABASE, user=USER, password=PASSWORD
        )
        cursor = conn.cursor()

        query = """
            INSERT INTO shifts (pa_ppl_id, date_time_in, date_time_out, payroll_period, shift_status)
            VALUES (%s)
        """
        execute_values(cursor, query, shifts)  # This is fast and safe

        # Commit the transaction
        conn.commit()

        print(f"Inserted data: {shifts}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        if conn:
            cursor.close()
            conn.close()
