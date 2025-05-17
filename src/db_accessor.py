import logging
import psycopg2
from psycopg2.extras import execute_values
import os
from src.configs import HOST, PORT

logger = logging.getLogger(__name__)


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

    print(f"Inserted data into aides: {aides}")  # Optional: just for logging


@with_db_connection
def add_shifts_to_db(cursor, conn, shifts):
    """
    For some traceability we are adding the data into two tables. Table shifts is
    the most current table. It will show the data at present. shift_history shows
    all the changes of the data over time. So if a shift's status goes from
    "Awaiting Approval" to "Paid" then shifts will show "Paid" (i.e. the most up to date info)

    and shift_history will show two records "Awaiting Approval" datetime and "Paid" datetime
    """
    query = """
            INSERT INTO shifts (pa_ppl_id, date_time_in, date_time_out, shift_status)
            VALUES %s
            ON CONFLICT (shift_id) DO UPDATE
            SET
                pa_ppl_id = EXCLUDED.pa_ppl_id,
                date_time_in = EXCLUDED.date_time_in,
                date_time_out = EXCLUDED.date_time_out,
                shift_status = EXCLUDED.shift_status;
        """
    execute_values(cursor, query, shifts)  # This is fast and safe

    print(f"Inserted data into shifts: {shifts}")  # Optional: just for logging

    query = """
            INSERT INTO shift_history (pa_ppl_id, date_time_in, date_time_out, shift_status)
            VALUES %s
        """
    execute_values(cursor, query, shifts)  # This is fast and safe

    print(f"Inserted data into shift_history: {shifts}")  # Optional: just for logging
