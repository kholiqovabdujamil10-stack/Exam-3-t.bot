from connection import *

async def created_ticket(telegram_id, subject):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO users (username, full_name, balance, telegram_id ) VALUES 
            ($1, $2, $3, $4)
        """, str(telegram_id), subject)

        return conn
    except Exception as error:
        print(f"Created user error: {error}")
    finally:
        await conn.close()


async def get_ticket(telegram_id):
    try:
        conn = await connection_db()
        ticket = await conn.fetchrow("""
            SELECT *
            FROM ticket
            WHERE telegram_id = $1
        """, str(telegram_id))
        return ticket
    
    except Exception as error:
        print(f"Get ticket error: {error}")

    finally:
        await conn.close()


async def get_tickets():
    try:
        conn = await connection_db()
        tickets = await conn.fetch("""
            SELECT * FROM tickets
        """)
        return tickets
    
    except Exception as error:
        print(f"Get tickets error: {error}")

    finally:
        await conn.close()


async def ticket_history(telegram_id):
    try:
        conn = await connection_db()
        ticket = await conn.fetch("""
            SELECT tickets.ticket_id, tickets.subject, tickets.created_at from tickets
            JOIN users
            ON tickets.ticket_id = ticket_replies.ticket_id
            WHERE tickets.telegram_id = $1
            ORDER BY tickets.tickets_id
        """, str(telegram_id))
        return ticket

    except Exception as error:
        print(f"Get tickets error: {error}")

    finally:
        await conn.close()


async def create_ticket(user_id, subject, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO (user_id, subject, telegram_id)
            VALUES ($1, $2, $3)
        """, user_id, subject, str(telegram_id))
        return conn

    except Exception as error:
        print(f"Create Ticket error: {error}")

    finally:
        await conn.close()