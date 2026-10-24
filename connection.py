import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

passw = os.getenv("PASSWORD_DB")


async def connection_db():
    return await asyncpg.connect(
        host="localhost",
        port=5432,
        user="postgres",
        database="lesson 1",
        password=passw
    )


async def create_table():
    try:
        conn = await connection_db()

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                full_name VARCHAR(100),
                telegram_id BIGINT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                is_active BOOLEAN DEFAULT TRUE
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                subject VARCHAR(200) NOT NULL,
                status VARCHAR(10) NOT NULL DEFAULT 'open'
                CHECK (status IN ('open', 'closed')),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS ticket_replies (
                reply_id SERIAL PRIMARY KEY,
                ticket_id INTEGER NOT NULL
                REFERENCES tickets(ticket_id)
                ON DELETE CASCADE,
                author VARCHAR(10) NOT NULL
                CHECK (author IN ('user', 'support')),
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        print("Database tables created successfully")

    except Exception as error:
        print(f"Database creation error: {error}")

    finally:
        await conn.close()
