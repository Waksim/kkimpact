import sqlite3


sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
cursor = sqlite_connection.cursor()


# cursor.execute("""SELECT * FROM main.hoyolab_decks
# WHERE EXISTS (
#   SELECT 1 FROM main.hoyolab_decks p2
#   WHERE main.hoyolab_decks.deck_id = p2.deck_id
#   AND main.hoyolab_decks.deck_code = p2.deck_code
#   AND main.hoyolab_decks.rowid > p2.rowid
# );""")

table_name = "hoyolab_decks_eng"

cursor.execute(f"""DELETE FROM main.{table_name}
WHERE EXISTS (
  SELECT 1 FROM main.{table_name} p2 
  WHERE main.{table_name}.deck_id = p2.deck_id
  AND main.{table_name}.deck_code = p2.deck_code
  AND main.{table_name}.rowid > p2.rowid
);""")
# action_cards = cursor.fetchall()

# print(len(action_cards))
sqlite_connection.commit()
cursor.close()
