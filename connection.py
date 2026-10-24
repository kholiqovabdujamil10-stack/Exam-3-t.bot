import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

passw = os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="Support Ticket System",
            password=passw
        )
        return conn
    except Exception as error:
        print(f"Database connection error: {error}")

async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
                CREATE TABLE IF NOT EXIST tickets(
                    ticket_id SERIAL PRIMARY KEY,
                    telegram_id VARCHAR(30),
                    subject VARCHAR(50),
                    status BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
            );
                CREATE TABLE IF NOT EXIST ticket_replies(
                    ticket_replies SERIAL PRIMARY KEY,
                    ticket_id INT REFERENCES tickets(ticket_id),
                    author varchar(30),
                    message VARCHAR(500),
                    created_at TIMESTAMP DEFAULT NOW()
            );
                           """)
        print("Database tables created successfully")
    except Exception as error:
        print(f"Database created error in {error}")
    finally:
        await conn.close()