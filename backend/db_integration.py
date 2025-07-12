import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv
import os
import logging
from contextlib import contextmanager

# Load .env variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create a connection pool once — reuse connections later
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="expense_pool",
        pool_size=5,
        pool_reset_session=True,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    logger.info("Connection pool created successfully")
except Error as e:
    logger.error(f"Error creating connection pool: {e}")
    raise

# Context manager: safely get & close connection
@contextmanager
def get_connection():
    conn = None
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            logger.info("DB connection acquired from pool")
            yield conn
    except Error as e:
        logger.error(f"DB error: {e}")
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()
            logger.info("DB connection returned to pool")

#functions using context manager

def fetch_expense_by_date(date):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM expenses WHERE expense_date = %s",
                (date,)
            )
            expenses = cursor.fetchall()
    return expenses

def update_expense_by_id(id, amount, category, notes):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE expenses SET amount=%s, category=%s, notes=%s WHERE id=%s",
                (amount, category, notes, id)
            )
            conn.commit()
            logger.info(f"Updated expense ID {id}: amount={amount}, category={category}, notes={notes}")


def fetch_expense_between_dates(start_date, end_date):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT category, SUM(amount) as total_sum
                FROM expenses
                WHERE expense_date BETWEEN %s AND %s
                GROUP BY category
            """
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
    return [{"category": row[0], "total_sum": row[1]} for row in results]

def insert_expense(expense_date, amount, category, notes):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                (expense_date, amount, category, notes)
            )
            conn.commit()
            logger.info(f"Inserted expense: {expense_date}, {amount}, {category}")

def delete_expense(column_name, value):
    allowed_columns = {"expense_date", "category", "amount", "notes", "id"}
    if column_name not in allowed_columns:
        raise ValueError(f"Invalid column: {column_name}")

    query = f"DELETE FROM expenses WHERE {column_name} = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (value,))
            conn.commit()
            logger.info(f"Deleted expense(s) where {column_name} = {value}")


