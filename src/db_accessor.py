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


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(
                host=HOST, port=PORT, dbname=DATABASE, user=USER, password=PASSWORD
            )
            cursor = conn.cursor()
            result = func(
                cursor, conn, *args, **kwargs
            )  # Pass both cursor and conn to the function
            conn.commit()  # Commit the transaction after the function execution
            return result
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return wrapper


@with_db_connection
def add_aides_to_db(cursor, conn, aides):
    query = """
        INSERT INTO aides (pa_ppl_id, pa_name)
        VALUES %s
        ON CONFLICT (pa_ppl_id) DO NOTHING
    """
    execute_values(cursor, query, aides)  # This is fast and safe

    print(f"Inserted data: {aides}")  # Optional: just for logging


@with_db_connection
def add_shifts_to_db(cursor, conn, shifts):
    query = """
            INSERT INTO shifts (pa_ppl_id, date_time_in, date_time_out, payroll_period, shift_status)
            VALUES %s
        """
    execute_values(cursor, query, shifts)  # This is fast and safe

    print(f"Inserted data: {shifts}")  # Optional: just for logging
