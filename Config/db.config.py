import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
load_dotenv()

from Utils.Color import GREEN, RESET


DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def setup_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Using UUID as PRIMARY KEY
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id UUID PRIMARY KEY,
            image_url TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print(f"{GREEN}Connected to Neon and verified table schema.{RESET}")
