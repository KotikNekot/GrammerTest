import aiosqlite

async def create_user_table():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,    
                visible_name TEXT DEFAULT '',           
                correct_words INTEGER DEFAULT 0,      
                show_in_leaderboard BOOLEAN DEFAULT 1 -- 
            )
        """)
        await db.commit()


async def create_user(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (id, correct_words, show_in_leaderboard)
            VALUES (?, 0, 1)
        """, (user_id,))
        await db.commit()


async def edit_show(user_id: int, show: bool):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            UPDATE users
            SET show_in_leaderboard = ?
            WHERE id = ?
        """, (int(show), user_id))
        await db.commit()

async def edit_name(user_id: int, name: str):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            UPDATE users
            SET visible_name = ?
            WHERE id = ?
        """, (name, user_id))
        await db.commit()


async def add_correct(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            UPDATE users
            SET correct_words = correct_words + 1
            WHERE id = ?
        """, (user_id,))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()

    users = [
        {
            "id": row[0],
            "visible_name": row[1],
            "correct_words": row[2],
            "show_in_leaderboard": bool(row[3])
        } for row in rows
    ]
    return users


async def get_user(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        await cursor.close()

    if row:
        return {
            "id": row[0],
            "visible_name": row[1],
            "correct_words": row[2],
            "show_in_leaderboard": bool(row[3])
        }
    return None
