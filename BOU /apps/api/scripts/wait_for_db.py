"""Wait for PostgreSQL to be ready."""
import time
import psycopg2
from app.core.config import settings

MAX_RETRIES = 30
for i in range(MAX_RETRIES):
    try:
        conn = psycopg2.connect(settings.DATABASE_URL_SYNC)
        conn.close()
        print("✅ Database is ready")
        break
    except psycopg2.OperationalError:
        print(f"⏳ Waiting for database... ({i+1}/{MAX_RETRIES})")
        time.sleep(2)
else:
    print("❌ Could not connect to database")
    exit(1)