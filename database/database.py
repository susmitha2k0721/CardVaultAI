import sqlite3
from datetime import datetime
import sqlite3
import os
import sys
from datetime import datetime

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DB_PATH = resource_path("database/cardvault.db")
def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,
        company TEXT,
        designation TEXT,
        phone TEXT,
        email TEXT,
        website TEXT,
        address TEXT,

        image_path TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        image_path TEXT,
        ocr_text TEXT,
        scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
def save_contact(data):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contacts
    (
        name,
        company,
        designation,
        phone,
        email,
        website,
        address,
        image_path
    )
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        data["name"],
        data["company"],
        data["designation"],
        data["phone"],
        data["email"],
        data["website"],
        data["address"],
        data["image_path"]
    ))

    conn.commit()
    conn.close()
def get_all_contacts():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        company,
        designation,
        phone,
        email,
        website,
        address,
        image_path
    FROM contacts
    ORDER BY id DESC
    """)

    contacts = cursor.fetchall()

    conn.close()

    return contacts
def save_scan_history(name, image_path, ocr_text):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO scan_history
    (
        name,
        image_path,
        ocr_text
    )
    VALUES
    (?, ?, ?)
    """,
    (
        name,
        image_path,
        ocr_text
    ))

    conn.commit()
    conn.close()
def get_scan_history():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, image_path, ocr_text, scan_time
        FROM scan_history
        WHERE id IN (
            SELECT MAX(id)
            FROM scan_history
            GROUP BY name
        )
        ORDER BY scan_time DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def search_contacts(keyword):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        company,
        designation,
        phone
    FROM contacts
    WHERE
        name LIKE ?
        OR company LIKE ?
        OR phone LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{keyword}%",
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows
def delete_contact(contact_id):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=?",
        (contact_id,)
    )

    conn.commit()
    conn.close()
from openpyxl import Workbook

def export_contacts_excel():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        company,
        designation,
        phone,
        email,
        website,
        address
    FROM contacts
    """)

    rows = cursor.fetchall()

    conn.close()

    wb = Workbook()

    ws = wb.active

    ws.title = "Contacts"

    headers = [
        "ID",
        "Name",
        "Company",
        "Designation",
        "Phone",
        "Email",
        "Website",
        "Address"
    ]

    ws.append(headers)

    for row in rows:
        ws.append(row)

    wb.save("exports/excel/contacts.xlsx")
from reportlab.platypus import SimpleDocTemplate, Table

def export_contacts_pdf():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        company,
        phone,
        email
    FROM contacts
    """)

    rows = cursor.fetchall()

    conn.close()

    filename = f"exports/pdf/contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "CardVault AI Contact Report",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    data = [
        [
            "ID",
            "Name",
            "Company",
            "Phone",
            "Email"
        ]
    ]

    for row in rows:
        data.append(list(row))

    table = Table(
        data,
        colWidths=[40, 120, 140, 100, 180]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
        ])
    )

    elements.append(table)

    pdf.build(elements)
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
def get_total_contacts():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM contacts"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total
def get_total_scans():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM scan_history"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total
def get_recent_contacts():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM contacts
    ORDER BY id DESC
    LIMIT 5
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_contact_by_id(contact_id):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contacts WHERE id=?",
        (contact_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row
def update_contact(
    contact_id,
    name,
    company,
    designation,
    phone,
    email,
    website,
    address
):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE contacts
    SET
        name=?,
        company=?,
        designation=?,
        phone=?,
        email=?,
        website=?,
        address=?
    WHERE id=?
    """,
    (
        name,
        company,
        designation,
        phone,
        email,
        website,
        address,
        contact_id
    ))

    conn.commit()

    conn.close()
def get_total_contacts():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM contacts")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_scans():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")

    total = cursor.fetchone()[0]

    conn.close()

    return total
def clear_scan_history():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM scan_history")

    conn.commit()

    conn.close()
def get_today_scans():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM scan_history
        WHERE DATE(scan_time) = DATE('now','localtime')
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total
def get_duplicate_count():

    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(count - 1)
        FROM (
            SELECT COUNT(*) AS count
            FROM scan_history
            GROUP BY name
            HAVING COUNT(*) > 1
        )
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0
def contact_exists(name, phone):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM contacts
        WHERE name = ? OR phone = ?
        LIMIT 1
    """, (name, phone))

    row = cursor.fetchone()

    conn.close()

    return row
def delete_scan_history(scan_id):

    import sqlite3

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM scan_history WHERE id=?",
        (scan_id,)
    )

    conn.commit()
    conn.close()