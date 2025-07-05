DROP TABLE IF EXISTS pelamar;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS lowongan;
DROP TABLE IF EXISTS kriteria;
DROP TABLE IF EXISTS subkriteria;
DROP TABLE IF EXISTS pelamar_lowongan;
DROP TABLE IF EXISTS lamaran;

-- Tabel pelamar (untuk login pelamar)
CREATE TABLE pelamar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  nama_lengkap TEXT,
  email TEXT,
  no_telp TEXT,
  alamat TEXT
);

-- Tabel lowongan
CREATE TABLE lowongan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nama_posisi TEXT NOT NULL,
  deskripsi TEXT,
  batas_akhir TEXT,
  informasi_pribadi TEXT  -- JSON list misalnya ["email", "no_telp"]
);

-- Tabel relasi pelamar dan lowongan
CREATE TABLE pelamar_lowongan (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelamar_id INTEGER NOT NULL,
  lowongan_id INTEGER NOT NULL,
  FOREIGN KEY (pelamar_id) REFERENCES pelamar(id),
  FOREIGN KEY (lowongan_id) REFERENCES lowongan(id)
);

-- Tabel lamaran
CREATE TABLE lamaran (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelamar_id INTEGER,
  lowongan_id INTEGER,
  tanggal_lamar DATE,
  status TEXT,
  dokumen TEXT,  -- JSON string simpan path CV/ijazah
  FOREIGN KEY (pelamar_id) REFERENCES pelamar(id),
  FOREIGN KEY (lowongan_id) REFERENCES lowongan(id)
);
