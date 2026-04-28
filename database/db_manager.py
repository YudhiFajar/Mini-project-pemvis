"""
database/db_manager.py
Modul pengelolaan database SQLite untuk Catatan Harian

Nama  : Yudhi Fajar Pratama
NIM   : F1D02310142
"""

import sqlite3
import os
from datetime import datetime


DB_PATH = "data/jurnal.db"


def get_connection():
    """Membuat dan mengembalikan koneksi ke database."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Akses kolom dengan nama
    return conn


def init_db():
    """Inisialisasi tabel database jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jurnal (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            judul       TEXT    NOT NULL,
            tanggal     TEXT    NOT NULL,
            mood        TEXT    NOT NULL,
            kategori    TEXT    NOT NULL,
            isi         TEXT    NOT NULL,
            cuaca       TEXT    NOT NULL,
            dibuat_pada TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


def tambah_jurnal(judul, tanggal, mood, kategori, isi, cuaca):
    """Menambahkan entri jurnal baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    dibuat_pada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO jurnal (judul, tanggal, mood, kategori, isi, cuaca, dibuat_pada)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (judul, tanggal, mood, kategori, isi, cuaca, dibuat_pada))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def ambil_semua_jurnal(keyword="", kategori="Semua", mood="Semua"):
    """Mengambil semua entri jurnal dengan filter opsional."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM jurnal WHERE 1=1"
    params = []

    if keyword:
        query += " AND (judul LIKE ? OR isi LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    if kategori != "Semua":
        query += " AND kategori = ?"
        params.append(kategori)

    if mood != "Semua":
        query += " AND mood = ?"
        params.append(mood)

    query += " ORDER BY tanggal DESC, id DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def ambil_jurnal_by_id(jurnal_id):
    """Mengambil satu entri jurnal berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jurnal WHERE id = ?", (jurnal_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_jurnal(jurnal_id, judul, tanggal, mood, kategori, isi, cuaca):
    """Memperbarui entri jurnal yang sudah ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jurnal
        SET judul=?, tanggal=?, mood=?, kategori=?, isi=?, cuaca=?
        WHERE id=?
    """, (judul, tanggal, mood, kategori, isi, cuaca, jurnal_id))
    conn.commit()
    conn.close()


def hapus_jurnal(jurnal_id):
    """Menghapus entri jurnal berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jurnal WHERE id = ?", (jurnal_id,))
    conn.commit()
    conn.close()


def statistik_jurnal():
    """Mengembalikan statistik ringkas dari semua jurnal."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM jurnal")
    total = cursor.fetchone()["total"]
    cursor.execute("SELECT mood, COUNT(*) as jumlah FROM jurnal GROUP BY mood ORDER BY jumlah DESC LIMIT 1")
    mood_row = cursor.fetchone()
    mood_terbanyak = mood_row["mood"] if mood_row else "-"
    cursor.execute("SELECT kategori, COUNT(*) as jumlah FROM jurnal GROUP BY kategori ORDER BY jumlah DESC LIMIT 1")
    kat_row = cursor.fetchone()
    kategori_terbanyak = kat_row["kategori"] if kat_row else "-"
    conn.close()
    return {"total": total, "mood_terbanyak": mood_terbanyak, "kategori_terbanyak": kategori_terbanyak}
