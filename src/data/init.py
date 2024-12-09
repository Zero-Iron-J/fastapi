"""sqlite 초기화"""

from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn : Connection | None = None
curs : Cursor | None = None

def create_db():
    global conn, curs
    top_dir = Path(__file__).resolve().parents[1]
    db_dir = top_dir / "db"
    db_dir.mkdir(exist_ok=True)
    db_name = "customer.db"
    db_path = str(db_dir/db_name)

    conn = connect(db_path, check_same_thread=False)
    curs = conn.cursor()

create_db()