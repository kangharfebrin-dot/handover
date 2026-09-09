# state.py
# Menyimpan state global aplikasi

class AppState:
    def __init__(self):
        # Info Kendaraan & Shift
        self.no_polisi = "R 9356 BM"
        self.shift = "Shift 1 - 04:30 WIB"
        
        # Checklist (menyimpan False jika "Tidak (Ada Kerusakan)", True jika "Baik / Ada")
        # 18 item MT (A. Perlengkapan Mobil Tangki)
        self.checklist_mt = {
            "Kondisi Rem": True,
            "Kondisi Ban": True,
            "Kondisi Wiper": True,
            "Kondisi Lampu-lampu": True,
            "Kondisi Kompartemen Tangki": True,
            "Keberadaan APAR": True,
            "Oli Mesin": True,
            "Air Radiator": True,
            "Keberadaan STNK": True,
            "Keberadaan Surat Keur": True,
            "Keberadaan Surat Tera": True,
            "Keberadaan Kotak P3K": True,
            "Keberadaan Flame Trap": True,
            "Keberadaan Ban Serep": True,
            "Keberadaan Tools Kit termasuk dongkrak": True,
            "Keberadaan Selang bongkar": True,
            "Keberadaan Grounding Cable": True,
            "Keberadaan Spill Kit": True,
        }
        
        # 10 item AMT (B. Perlengkapan AMT)
        self.checklist_amt = {
            "Membawa SIM Sesuai dengan Jenis Kendaraan": True,
            "Surat Ijin Masuk TBBM Masih Berlaku": True,
            "Menggunakan Seragam Kerja": True,
            "Menggunakan Safety Shoes": True,
            "Menggunakan Safety Helm": True,
            "Menggunakan ID Card": True,
            "Menggunakan Safety Glove (Sarung Tangan)": True,
            "Membawa Jas Hujan": True,
            "Membawa Buku Saku Service Excellent AMT": True,
            "Membawa Catatan Perjalanan AMT": True,
        }
        
        # ODO & Evaluasi
        self.odo_awal = "142.850"
        self.odo_akhir = "142.980"
        self.kategori_evaluasi = "Normal / Sesuai" # "Normal / Sesuai", "Minor (Catat)", "Mayor (Stop)"
        self.catatan = "Semua 28 item perlengkapan kendaraan & personil lengkap serta berfungsi optimal. MT siap beroperasi."
        
        # Verifikasi Tanda Tangan Shift
        self.verifikasi = {
            "pengemudi": {"title": "Pengemudi AMT 1", "name": "Budi Santoso", "status": True},
            "pengawas": {"title": "Pengawas AMT", "name": "Hendra S. (Pws)", "status": True},
            "hsse": {"title": "Petugas HSSE", "name": "Rahmat D.", "status": True},
        }

    def reset(self):
        self.__init__()

state = AppState()
