from connection import connection_db


async def created_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO users (username, full_name, telegram_id)
            VALUES ($1, $2, $3)
        """, username, full_name, int(telegram_id))
        return True
    except Exception as error:
        print(f"Create user error: {error}")
    finally:
        await conn.close()


async def get_user(telegram_id):
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
            SELECT * FROM users WHERE telegram_id = $1
        """, int(telegram_id))
    except Exception as error:
        print(f"Get user error: {error}")
    finally:
            await conn.close()


async def create_ticket(telegram_id, subject):
    try:
        conn = await connection_db()
        ticket_id = await conn.fetchval("""
            INSERT INTO tickets (user_id, subject)
            VALUES ($1, $2)
        """, int(telegram_id), subject)
        return ticket_id
    except Exception as error:
        print(f"Create ticket error: {error}")
    finally:
            await conn.close()


async def get_ticket(ticket_id):
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
            SELECT * FROM tickets WHERE ticket_id = $1
        """, int(ticket_id))
    except Exception as error:
        print(f"Get ticket error: {error}")
    finally:
            await conn.close()


async def get_user_tickets(telegram_id):
    try:
        conn = await connection_db()
        return await conn.fetch("""
            SELECT * FROM tickets
            WHERE user_id = $1
            ORDER BY ticket_id DESC
        """, int(telegram_id))
    except Exception as error:
        print(f"Get tickets error: {error}")
    finally:
            await conn.close()


async def add_reply(ticket_id, author, message):
    try:
        conn = await connection_db()
        ticket = await conn.fetchrow("""
            SELECT status FROM tickets WHERE ticket_id = $1
        """, int(ticket_id))

        if ticket and ticket["status"] == "open":
            await conn.execute("""
                INSERT INTO ticket_replies (ticket_id, author, message)
                VALUES ($1, $2, $3)
            """, int(ticket_id), author, message)
            return True

        return False
    except Exception as error:
        print(f"Add reply error: {error}")
    finally:
            await conn.close()


async def ticket_history(ticket_id):
    try:
        conn = await connection_db()
        return await conn.fetch("""
            SELECT * FROM ticket_replies
            WHERE ticket_id = $1
            ORDER BY created_at ASC
        """, int(ticket_id))
    except Exception as error:
        print(f"Ticket history error: {error}")
    finally:
            await conn.close()


async def close_ticket(ticket_id):
    try:
        conn = await connection_db()
        result = await conn.execute("""
            UPDATE tickets SET status = 'closed'
            WHERE ticket_id = $1 AND status = 'open'
        """, int(ticket_id))
        return result == "UPDATE 1"
    except Exception as error:
        print(f"Close ticket error: {error}")
    finally:
            await conn.close()