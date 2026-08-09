import sqlite3

conn = sqlite3.connect("database/cardvault.db")

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM contacts")

count = cursor.fetchone()[0]

print("Total Contacts:", count)

conn.close()