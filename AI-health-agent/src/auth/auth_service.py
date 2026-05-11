import hashlib
import re
import secrets
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st


class AuthService:
    def __init__(self):
        self.db_path = self._get_db_path()
        self._init_db()

        if "auth_token" in st.session_state:
            self.validate_session_token()

    def _get_db_path(self):
        project_root = Path(__file__).resolve().parents[2]
        db_dir = project_root / "data"
        db_dir.mkdir(exist_ok=True)
        return db_dir / "health_agent.sqlite3"

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    name TEXT,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS chat_messages (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    content TEXT,
                    role TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id
                    ON chat_sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id
                    ON chat_messages(session_id);
                """
            )

    def _row_to_dict(self, row):
        return dict(row) if row else None

    def _public_user(self, row):
        user = self._row_to_dict(row)
        if not user:
            return None
        user.pop("password_hash", None)
        user.pop("password_salt", None)
        return user

    def _hash_password(self, password, salt=None):
        salt = salt or secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 120000
        ).hex()
        return salt, password_hash

    def try_restore_session(self):
        return None

    def validate_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    def check_existing_user(self, email):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE lower(email) = lower(?)",
                (email,),
            ).fetchone()
        return row is not None

    def sign_up(self, email, password, name):
        try:
            if self.check_existing_user(email):
                return False, "Email already registered"

            user_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()
            salt, password_hash = self._hash_password(password)

            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO users (id, email, name, password_hash, password_salt, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, email.strip().lower(), name, password_hash, salt, created_at),
                )
                user = conn.execute(
                    "SELECT id, email, name, created_at FROM users WHERE id = ?",
                    (user_id,),
                ).fetchone()

            user_data = self._public_user(user)
            st.session_state.auth_token = secrets.token_urlsafe(32)
            st.session_state.user = user_data
            return True, user_data
        except sqlite3.IntegrityError:
            return False, "Email already registered"
        except Exception as e:
            return False, f"Sign up failed: {str(e)}"

    def sign_in(self, email, password):
        try:
            with self._connect() as conn:
                user = conn.execute(
                    "SELECT * FROM users WHERE lower(email) = lower(?)",
                    (email.strip(),),
                ).fetchone()

            if not user:
                return False, "Invalid email or password"

            _, password_hash = self._hash_password(password, user["password_salt"])
            if not secrets.compare_digest(password_hash, user["password_hash"]):
                return False, "Invalid email or password"

            user_data = self._public_user(user)
            st.session_state.auth_token = secrets.token_urlsafe(32)
            st.session_state.user = user_data
            return True, user_data
        except Exception as e:
            return False, str(e)

    def sign_out(self):
        try:
            from auth.session_manager import SessionManager

            SessionManager.clear_session_state()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_user(self):
        return st.session_state.get("user")

    def create_session(self, user_id, title=None):
        try:
            current_time = datetime.now()
            default_title = f"{current_time.strftime('%d-%m-%Y')} | {current_time.strftime('%H:%M:%S')}"
            session_id = str(uuid.uuid4())
            created_at = current_time.isoformat()

            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO chat_sessions (id, user_id, title, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (session_id, user_id, title or default_title, created_at),
                )
                session = conn.execute(
                    "SELECT * FROM chat_sessions WHERE id = ?",
                    (session_id,),
                ).fetchone()

            return True, self._row_to_dict(session)
        except Exception as e:
            return False, str(e)

    def get_user_sessions(self, user_id):
        try:
            with self._connect() as conn:
                sessions = conn.execute(
                    """
                    SELECT * FROM chat_sessions
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    """,
                    (user_id,),
                ).fetchall()
            return True, [self._row_to_dict(session) for session in sessions]
        except Exception as e:
            st.error(f"Error fetching sessions: {str(e)}")
            return False, []

    def save_chat_message(self, session_id, content, role="user"):
        try:
            message_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()

            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO chat_messages (id, session_id, content, role, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (message_id, session_id, content, role, created_at),
                )
                message = conn.execute(
                    "SELECT * FROM chat_messages WHERE id = ?",
                    (message_id,),
                ).fetchone()

            return True, self._row_to_dict(message)
        except Exception as e:
            return False, str(e)

    def get_session_messages(self, session_id):
        try:
            with self._connect() as conn:
                messages = conn.execute(
                    """
                    SELECT * FROM chat_messages
                    WHERE session_id = ?
                    ORDER BY created_at
                    """,
                    (session_id,),
                ).fetchall()
            return True, [self._row_to_dict(message) for message in messages]
        except Exception as e:
            return False, str(e)

    def delete_session(self, session_id):
        try:
            with self._connect() as conn:
                conn.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
            return True, None
        except Exception as e:
            st.error(f"Failed to delete session: {str(e)}")
            return False, str(e)

    def validate_session_token(self):
        user_id = st.session_state.get("user", {}).get("id")
        if not user_id:
            return None
        return self.get_user_data(user_id)

    def get_user_data(self, user_id):
        try:
            with self._connect() as conn:
                user = conn.execute(
                    "SELECT id, email, name, created_at FROM users WHERE id = ?",
                    (user_id,),
                ).fetchone()
            return self._public_user(user)
        except Exception:
            return None
