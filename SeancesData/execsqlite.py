from pathlib import Path
import sqlite3

with sqlite3.connect(Path(__file__).with_name("velolyon.db")) as conn:
    conn.executescript(Path("SeancesData/reqtmp.sql").read_text(encoding="utf-8"))