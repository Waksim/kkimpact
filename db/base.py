import os
import sqlite3
from typing import Tuple, Iterable

from aiogram import types


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "tcgCodes.sqlite")


class KkiDb:
    def __init__(self, db_path=None):
        db_path = db_path or DB_PATH
        self.connection = sqlite3.connect(db_path)

    def __del__(self):
        self.connection.close()

    def _fetch_query(self, query: str, params: Tuple = tuple()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.close()
        return data

    def _execute_query(self, query: str, params: Tuple = tuple()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def get_user_exists(self, user_id):
        return self._fetch_query(
            "SELECT EXISTS(SELECT * FROM telegram_users where tg_id = ?)",
            (user_id,),
        )

    def insert_user_info(self, message: types.Message):
        self._execute_query(
            "INSERT INTO telegram_users (tg_id, nickname, username, tg_lang, premium) VALUES (?, ?, ?, ?, ?);",
            (
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.username,
                message.from_user.language_code,
                message.from_user.is_premium,
            ),
        )

    def get_role_card_names(self, role_card_string, lang):
        return self._fetch_query(
            f"SELECT card_name_{lang} FROM main.role_cards WHERE {role_card_string}"
        )

    def get_role_cards(self, lang):
        return self._fetch_query(
            f"SELECT id, code, element, {lang} FROM main.role_cards"
        )

    def get_action_cards(self, role_card_ids: Iterable, resonances: Iterable):
        return self._fetch_query(
            "SELECT code FROM main.action_cards_2x WHERE (link_with_char = 0 OR link_with_char IN (?, ?, ?)) AND (resonance = 0 OR resonance IN (?, ?, ?, ?))",
            (*role_card_ids, *resonances),
        )

    def get_role_card_element(self, role_card):
        return self._fetch_query(
            f"SELECT element FROM main.role_cards WHERE ? = code",
            (role_card,),
        )

    def set_user_preferences(self, user_id, lang):
        self._execute_query(
            f"UPDATE telegram_users SET preferens = '{lang}' WHERE tg_id = ?",
            (user_id,),
        )

    def get_hoyolab_random_deck(self, table_lang):
        return self._fetch_query(
            f"SELECT * FROM {table_lang} ORDER BY RANDOM() LIMIT 1"
        )

    def get_role_card_code_by_sticker_uid(self, sticker_uid):
        return self._fetch_query(
            f"SELECT code FROM main.role_cards WHERE sticker_uid = '{sticker_uid}'"
        )
