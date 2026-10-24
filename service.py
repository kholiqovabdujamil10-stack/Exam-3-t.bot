from connection import *
import connection



async def created_user(username, full_name, telegram_id):
    conn = None
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO users (username, full_name, telegram_id)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING
        """, username, full_name, int(telegram_id))
        return True
    except Exception as error:
        print(f"Create user error: {error}")
        return False
    finally:
        if conn is not None:
            await conn.close()


async def get_user(telegram_id):
    conn = None
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
            SELECT * FROM users WHERE telegram_id = $1
        """, int(telegram_id))
    except Exception as error:
        print(f"Get user error: {error}")
        return None
    finally:
        if conn is not None:
            await conn.close()


async def create_ticket(telegram_id, subject):
    conn = None
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO tickets (user_id, subject)
            VALUES ($1, $2)
        """, int(telegram_id), subject)
        return True
    except Exception as error:
        print(f"Create ticket error: {error}")
        return False
    finally:
        if conn is not None:
            await conn.close()


async def get_ticket(ticket_id):
    conn = None
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
            SELECT * FROM tickets WHERE ticket_id = $1
        """, int(ticket_id))
    except Exception as error:
        print(f"Get ticket error: {error}")
        return None
    finally:
        if conn is not None:
            await conn.close()


async def get_user_tickets(telegram_id):
    conn = None
    try:
        conn = await connection_db()
        return await conn.fetch("""
            SELECT * FROM tickets
            WHERE user_id = $1
            ORDER BY ticket_id DESC
        """, int(telegram_id))
    except Exception as error:
        print(f"Get tickets error: {error}")
        return []
    finally:
        if conn is not None:
            await conn.close()


async def add_reply(ticket_id, author, message):
    conn = None
    try:
        conn = await connection_db()

        result = await conn.execute("""
            INSERT INTO ticket_replies (ticket_id, author, message)
            SELECT ticket_id, $2, $3
            FROM tickets
            WHERE ticket_id = $1 AND status = 'open'
        """, int(ticket_id), author, message)

        return result == "INSERT 0 1"

    except Exception as error:
        print(f"Add reply error: {error}")
        return False
    finally:
        if conn is not None:
            await conn.close()


async def ticket_history(ticket_id):
    conn = None
    try:
        conn = await connection_db()
        return await conn.fetch("""
            SELECT * FROM ticket_replies
            WHERE ticket_id = $1
            ORDER BY created_at ASC, reply_id ASC
        """, int(ticket_id))
    except Exception as error:
        print(f"Ticket history error: {error}")
        return []
    finally:
        if conn is not None:
            await conn.close()


async def close_ticket(ticket_id):
    conn = None
    try:
        conn = await connection_db()
        result = await conn.execute("""
            UPDATE tickets SET status = 'closed'
            WHERE ticket_id = $1 AND status = 'open'
        """, int(ticket_id))
        return result == "UPDATE 1"
    except Exception as error:
        print(f"Close ticket error: {error}")
        return False
    finally:
        if conn is not None:
            await conn.close()


async def create_table():
    await connection.create_table()