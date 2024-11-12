import psycopg2
import os

def get_database_connection():
    """Connect to the PostgreSQL database server."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

# def init_database():
#     """Initialize the database."""
#     conn = get_database_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS achievements (
#             id SERIAL PRIMARY KEY,
#             description TEXT NOT NULL,
#             points INTEGER NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit()
#     cur.close()
#     conn.close()

def add_achievement(description, points):
    """Add an achievement to the database."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO achievements (description, points) VALUES (%s, %s)",
        (description, points)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_achievements():
    """Get all achievements from the database."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM achievements ORDER BY created_at DESC")
    achievements = cur.fetchall()
    cur.close()
    conn.close()
    return achievements

def delete_all_achievements():
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM achievements")
    conn.commit()
    cur.close()
    conn.close()
    
def delete_achievement(achievement_id):
    """Delete a specific achievement by its ID."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM achievements WHERE id = %s", (achievement_id,))
    conn.commit()
    cur.close()
    conn.close()