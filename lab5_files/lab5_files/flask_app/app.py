from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Initialize Redis
r = redis.Redis(host="redis", port=6379)

# PostgreSQL setup
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'db'),
        database=os.getenv('POSTGRES_DB', 'mydb'),
        user=os.getenv('POSTGRES_USER', 'myuser'),
        password=os.getenv('POSTGRES_PASSWORD', 'mypassword')
    )
    return conn

# Initialize the database table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_visits (
            id SERIAL PRIMARY KEY,
            visit_count INTEGER NOT NULL
        );
    ''')
    cursor.execute('''
        INSERT INTO page_visits (id, visit_count) VALUES (1, 0) ON CONFLICT (id) DO NOTHING;
    ''')
    conn.commit()
    conn.close()

# Record and return page visits
@app.route("/")
def home():
    # Increment Redis counter
    count = r.incr("hits")
    
    # Update PostgreSQL counter
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE page_visits SET visit_count = visit_count + 1 WHERE id = 1;")
    cursor.execute("SELECT visit_count FROM page_visits WHERE id = 1;")
    visit_count = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return f"This page has been visited {visit_count} times (stored in PostgreSQL), {count} times (stored in Redis)."

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
