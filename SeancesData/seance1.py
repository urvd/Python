import sqlite3, csv, io

CLIENTS_CSV = """client_id,email,nom,ville,date_inscription
1,alice@mail.fr,Alice Martin,Lyon,2026-01-05
2,bruno@mail.fr,Bruno Petit,Lyon,2026-01-12
3,chloe@mail.fr,Chloé Durand,Villeurbanne,2026-02-03
4,david@mail.fr,David Moreau,Lyon,2026-02-20
5,alice@mail.fr,Alice M.,Lyon,2026-03-01
6,emma@mail.fr,,Bron,2026-03-08
7,farid@mail.fr,Farid Benali,Lyon,2026-03-15
8,gaelle@mail.fr,Gaëlle Roux,Villeurbanne,2026-04-02
"""
STATIONS_CSV = """station_id,nom,capacite
1,Bellecour,20
2,Part-Dieu,30
3,Croix-Rousse,0
4,Confluence,15
"""
VELOS_CSV = """velo_id,type,station_id
101,mecanique,1
102,electrique,1
103,electrique,2
104,mecanique,2
105,cargo,4
106,electrique,4
107,mecanique,9
"""
LOCATIONS_CSV = """location_id,client_id,velo_id,debut,fin,montant
1001,1,101,2026-04-01 08:00,2026-04-01 08:25,1.50
1002,2,102,2026-04-01 09:10,2026-04-01 09:55,3.20
1003,3,103,2026-04-02 17:30,2026-04-02 18:05,2.80
1004,1,104,2026-04-03 07:45,2026-04-03 08:10,1.50
1005,4,106,2026-04-03 12:00,2026-04-03 11:30,2.00
1006,7,101,2026-04-04 18:00,2026-04-04 18:40,2.40
1007,42,102,2026-04-05 10:00,2026-04-05 10:20,1.60
1008,8,103,2026-04-05 14:00,2026-04-05 14:50,4.00
1009,2,106,2026-04-06 08:15,2026-04-06 08:45,-2.50
1010,3,104,2026-04-06 19:00,,
1011,4,102,2026-04-07 07:30,2026-04-07 08:00,2.40
1012,1,103,2026-04-07 18:20,2026-04-07 19:00,3.20
"""

DDL = """
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    nom TEXT,
    ville TEXT,
    date_inscription TEXT NOT NULL
);

CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    capacite INTEGER NOT NULL
);

CREATE TABLE velos (
    velo_id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    station_id INTEGER NOT NULL,
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);

CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    velo_id INTEGER NOT NULL,
    debut TEXT NOT NULL,
    fin TEXT,
    montant REAL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (velo_id) REFERENCES velos(velo_id)
);
"""

def connecter(chemin="SeancesData/velolyon.db"):
    con = sqlite3.connect(chemin)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def charger(con, table, texte_csv):
    inserees, rejets = 0, []
    reader = csv.DictReader(io.StringIO(texte_csv))
    colonnes = list(reader.fieldnames or [])
    for ligne in reader:
        valeurs = {cle: (None if val == "" else val) for cle, val in ligne.items()}
        champs = [c for c in colonnes if c in valeurs]
        try:
            con.execute(
                f"INSERT INTO {table} ({', '.join(champs)}) VALUES ({', '.join(['?'] * len(champs))})",
                [valeurs[c] for c in champs],
            )
            inserees += 1
        except sqlite3.IntegrityError as err:
            identifiant = None
            for cle in ["client_id", "station_id", "velo_id", "location_id"]:
                if cle in valeurs and valeurs[cle] is not None:
                    identifiant = valeurs[cle]
                    break
            rejets.append((identifiant, str(err)))
    print(f"{table}: {inserees} insérées, {len(rejets)} rejetées")
    for r in rejets:
        print("   ", r)


if __name__ == "__main__":
    con = connecter("velolyon.db")
    con.executescript(DDL)
    for table, data in [("clients", CLIENTS_CSV), ("stations", STATIONS_CSV),
                        ("velos", VELOS_CSV), ("locations", LOCATIONS_CSV)]:
        charger(con, table, data)
    con.commit()
    total_locations, somme_montants = con.execute(
        "SELECT COUNT(*), COALESCE(SUM(montant), 0) FROM locations"
    ).fetchone()
    print(f"locations: {total_locations}, somme montants: {somme_montants}")
    con.close()