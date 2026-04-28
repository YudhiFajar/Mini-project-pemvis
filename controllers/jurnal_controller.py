"""
controllers/jurnal_controller.py
Controller yang menghubungkan View dengan Database

Nama  : Yudhi Fajar Pratama
NIM   : F1D02310142
"""

from database import db_manager


class JurnalController:
    """Controller untuk operasi CRUD jurnal harian."""

    def __init__(self):
        # Inisialisasi database saat controller dibuat
        db_manager.init_db()

    def tambah(self, judul, tanggal, mood, kategori, isi, cuaca):
        """Memvalidasi dan menambahkan jurnal baru."""
        if not judul.strip():
            raise ValueError("Judul tidak boleh kosong.")
        if not isi.strip():
            raise ValueError("Isi jurnal tidak boleh kosong.")
        if not tanggal:
            raise ValueError("Tanggal harus diisi.")
        return db_manager.tambah_jurnal(judul.strip(), tanggal, mood, kategori, isi.strip(), cuaca)

    def ambil_semua(self, keyword="", kategori="Semua", mood="Semua"):
        """Mengambil semua jurnal dengan filter."""
        return db_manager.ambil_semua_jurnal(keyword, kategori, mood)

    def ambil_by_id(self, jurnal_id):
        """Mengambil jurnal berdasarkan ID."""
        return db_manager.ambil_jurnal_by_id(jurnal_id)

    def update(self, jurnal_id, judul, tanggal, mood, kategori, isi, cuaca):
        """Memvalidasi dan memperbarui jurnal."""
        if not judul.strip():
            raise ValueError("Judul tidak boleh kosong.")
        if not isi.strip():
            raise ValueError("Isi jurnal tidak boleh kosong.")
        db_manager.update_jurnal(jurnal_id, judul.strip(), tanggal, mood, kategori, isi.strip(), cuaca)

    def hapus(self, jurnal_id):
        """Menghapus jurnal berdasarkan ID."""
        db_manager.hapus_jurnal(jurnal_id)

    def statistik(self):
        """Mengambil statistik jurnal."""
        return db_manager.statistik_jurnal()
