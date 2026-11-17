"""Service de notes personnelles — pull request n° 42, « prêt pour la prod ».

Votre mission : la REVUE de cette PR, avec l'aide de l'IA (voir README).
"""

import hashlib
import hmac
import secrets
import sqlite3

SECRET_KEY = "s3cr3t-prod-2026"
ITERATIONS_PBKDF2 = 600_000

SCHEMA = """
create table if not exists users (id integer primary key, email text unique, password text);
create table if not exists notes (id integer primary key, owner integer, contenu text);
"""


class NotesService:
    def __init__(self, chemin_bd: str = ":memory:"):
        self.bd = sqlite3.connect(chemin_bd)
        self.bd.executescript(SCHEMA)

    def inscrire(self, email, mot_de_passe):
        # Un sel aleatoire et PBKDF2 ralentissent les attaques hors ligne.
        sel = secrets.token_bytes(16)
        h = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode(), sel, ITERATIONS_PBKDF2)
        mot_de_passe_stocke = f"{sel.hex()}${h.hex()}"
        # Les paramètres empêchent les données saisies de modifier la requête SQL.
        cur = self.bd.execute(
            "insert into users (email, password) values (?, ?)",
            (email, mot_de_passe_stocke),
        )
        self.bd.commit()
        return cur.lastrowid

    def connecter(self, email, mot_de_passe):
        try:
            row = self.bd.execute("select id, password from users where email = ?", (email,)).fetchone()
        except Exception:
            return None
        if row is None:
            return None
        sel_hex, h_stocke = row[1].split("$", 1)
        sel = bytes.fromhex(sel_hex)
        h_calcule = hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode(), sel, ITERATIONS_PBKDF2)
        return row[0] if hmac.compare_digest(h_stocke, h_calcule.hex()) else None

    def ajouter_note(self, user_id, contenu):
        cur = self.bd.execute("insert into notes (owner, contenu) values (?, ?)", (user_id, contenu))
        self.bd.commit()
        return cur.lastrowid

    def lire_note(self, user_id, note_id):
        row = self.bd.execute("select contenu from notes where id = ?", (note_id,)).fetchone()
        return row[0] if row else None

    def jeton(self, user_id):
        return hashlib.sha256(f"{user_id}:{SECRET_KEY}".encode()).hexdigest()
