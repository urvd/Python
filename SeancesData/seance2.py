import csv, io, sqlite3
from pathlib import Path

con = sqlite3.connect(Path(__file__).with_name("velolyon.db"))
con.execute("PRAGMA foreign_keys = ON")

# --- Séance 1 : schéma + données de référence (relançable) ---
con.executescript("""
CREATE TABLE IF NOT EXISTS clients (
  client_id INTEGER PRIMARY KEY,
  email     TEXT NOT NULL UNIQUE,
  nom       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS stations (
  station_id INTEGER PRIMARY KEY,
  nom        TEXT NOT NULL UNIQUE,
  capacite   INTEGER NOT NULL CHECK (capacite > 0)
);
CREATE TABLE IF NOT EXISTS velos (
  velo_id    INTEGER PRIMARY KEY,
  type       TEXT NOT NULL CHECK (type IN ('classique','electrique')),
  station_id INTEGER REFERENCES stations(station_id)
);
CREATE TABLE IF NOT EXISTS locations (
  location_id INTEGER PRIMARY KEY,
  client_id   INTEGER NOT NULL REFERENCES clients(client_id),
  velo_id     INTEGER NOT NULL REFERENCES velos(velo_id),
  debut       TEXT NOT NULL,
  fin         TEXT,
  CHECK (fin IS NULL OR fin > debut)
);
INSERT OR IGNORE INTO clients VALUES (1,'alice@mail.fr','Alice'),(2,'bruno@mail.fr','Bruno'),
  (3,'chloe@mail.fr','Chloé'),(4,'david@mail.fr','David');
INSERT OR IGNORE INTO stations VALUES (1,'Bellecour',20),(2,'Part-Dieu',30),(3,'Croix-Rousse',12);
INSERT OR IGNORE INTO velos VALUES (1,'classique',1),(2,'electrique',1),(3,'classique',2),
  (4,'electrique',2),(5,'classique',3);
INSERT OR IGNORE INTO locations VALUES
  (1,1,1,'2026-10-01 08:00:00','2026-10-01 08:40:00'),
  (2,2,2,'2026-10-01 09:15:00','2026-10-01 10:05:00'),
  (3,1,3,'2026-10-02 18:00:00','2026-10-02 18:25:00'),
  (4,3,4,'2026-10-03 07:30:00','2026-10-03 08:10:00'),
  (5,4,5,'2026-10-03 12:00:00','2026-10-03 12:45:00'),
  (6,2,2,'2026-10-04 17:00:00','2026-10-04 17:50:00'),
  (7,3,1,'2026-10-05 08:05:00',NULL);
""")

# --- Séance 2 : schéma ---
con.executescript("""
CREATE TABLE IF NOT EXISTS paiements (
  paiement_id   INTEGER PRIMARY KEY,
  location_id   INTEGER NOT NULL REFERENCES locations(location_id),
  montant       REAL    NOT NULL CHECK (montant > 0),
  moyen         TEXT    NOT NULL CHECK (moyen IN ('CB','APPLE_PAY','ESPECES')),
  date_paiement TEXT    NOT NULL
                CHECK (date_paiement IS strftime('%Y-%m-%d %H:%M:%S', date_paiement)),
  statut        TEXT    NOT NULL DEFAULT 'OK' CHECK (statut IN ('OK','REMBOURSE'))
);
CREATE TABLE IF NOT EXISTS options (
  option_id INTEGER PRIMARY KEY,
  libelle   TEXT NOT NULL UNIQUE,
  prix      REAL NOT NULL CHECK (prix >= 0)
);
CREATE TABLE IF NOT EXISTS location_options (
  location_id INTEGER NOT NULL REFERENCES locations(location_id),
  option_id   INTEGER NOT NULL REFERENCES options(option_id),
  PRIMARY KEY (location_id, option_id)
);
CREATE TABLE IF NOT EXISTS erreurs_chargement (
  erreur_id    INTEGER PRIMARY KEY,
  table_cible  TEXT    NOT NULL,
  numero_ligne INTEGER NOT NULL,
  contenu      TEXT,
  raison       TEXT    NOT NULL,
  charge_le    TEXT    NOT NULL DEFAULT (datetime('now'))
);
""")

options = [(1,'casque',0.0),(2,'siege_enfant',2.0),(3,'assurance',1.5)]
location_options = [(1,1),(2,3),(4,1),(4,3),(6,2)]
with con:
    con.executemany("INSERT OR IGNORE INTO options VALUES (?,?,?)", options)
    con.executemany("INSERT OR IGNORE INTO location_options VALUES (?,?)", location_options)

paiements_csv = """paiement_id,location_id,montant,moyen,date_paiement,statut
1,1,2.50,CB,2026-10-01 08:41:00,OK
2,2,4.00,APPLE_PAY,2026-10-01 10:06:00,OK
3,3,2.00,CB,2026-10-02 18:26:00,OK
4,4,3.50,CB,03/10/2026 08:11,OK
5,5,3.00,ESPECES,2026-10-03 12:46:00,OK
6,6,4.50,CB,2026-10-04 17:51:00,OK
7,6,-4.50,CB,2026-10-04 18:30:00,REMBOURSE
8,99,2.00,CB,2026-10-05 09:00:00,OK
9,2,1.00,CHEQUE,2026-10-01 10:10:00,OK
10,4,3.50,CB,2026-10-03 08:11:00,OK
11,5,,CB,2026-10-03 12:50:00,OK
12,1,2.50,CB,2026-10-01 08:41:00,OK
"""

# --- Chargement : rechargement complet et atomique ---
SQL_INS = "INSERT INTO paiements VALUES (?,?,?,?,?,?)"
SQL_ERR = ("INSERT INTO erreurs_chargement (table_cible, numero_ligne, contenu, raison) "
           "VALUES ('paiements', ?, ?, ?)")
ok = ko = 0
with con:                                   # une seule transaction : tout ou rien + commit final
    con.execute("DELETE FROM paiements")
    con.execute("DELETE FROM erreurs_chargement WHERE table_cible = 'paiements'")
    for n, ligne in enumerate(csv.DictReader(io.StringIO(paiements_csv)), start=1):
        valeurs = (ligne["paiement_id"], ligne["location_id"], ligne["montant"] or None,
                   ligne["moyen"], ligne["date_paiement"], ligne["statut"])
        try:
            con.execute(SQL_INS, valeurs)   # en cas d'échec, seul CET INSERT est annulé
            ok += 1
        except sqlite3.IntegrityError as e:
            con.execute(SQL_ERR, (n, ",".join(ligne.values()), str(e)))
            ko += 1
print(f"{ok} chargées / {ko} rejetées")

print(con.execute("SELECT COUNT(*) FROM paiements").fetchone())
for r in con.execute("SELECT numero_ligne, raison FROM erreurs_chargement ORDER BY numero_ligne"):
    print(r)
print(con.execute("""SELECT o.libelle, COUNT(*) FROM location_options lo
                     JOIN options o USING(option_id) GROUP BY o.libelle ORDER BY o.libelle""").fetchall())
print(con.execute("SELECT ROUND(SUM(montant),2) FROM paiements").fetchone())
try:
    con.execute("INSERT INTO location_options VALUES (4,1)")
except sqlite3.IntegrityError as e:
    print("Doublon N-N :", e)
con.close()