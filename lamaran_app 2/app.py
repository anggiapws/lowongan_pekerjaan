from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
import hashlib
import os
import json

app = Flask(__name__)
app.secret_key = 'secretkey123'
DB_PATH = 'database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE pelamar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nama_lengkap TEXT NOT NULL,
                    email TEXT NOT NULL,
                    no_telp TEXT NOT NULL
                )
            """)
        print("Database dan tabel pelamar berhasil dibuat.")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Login Admin
        if username == 'admin' and password == 'admin123':
            session['user_role'] = 'admin'
            session['user_username'] = username
            flash("Login sebagai Admin berhasil.")
            return redirect(url_for('admin_dashboard'))

        # Login Pelamar
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pelamar WHERE username=? AND password=?", 
                        (username, hash_password(password)))
            pelamar = cur.fetchone()

        if pelamar:
            session['user_role'] = 'pelamar'
            session['user_username'] = username
            flash("Login berhasil.")
            return redirect(url_for('pelamar_dashboard'))

        flash('Login gagal, username atau password salah.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ambil data dari form
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        nama_lengkap = request.form['nama_lengkap'].strip()
        email = request.form['email'].strip()
        no_telp = request.form['no_telp'].strip()

        # validasi sederhana
        if not all([username, password, nama_lengkap, email, no_telp]):
            flash("Semua field wajib diisi.")
            return redirect(url_for('register'))

        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pelamar WHERE username=?", (username,))
            if cur.fetchone():
                flash("Username sudah terdaftar.")
                return redirect(url_for('register'))

            # simpan data pelamar
            cur.execute("""
                INSERT INTO pelamar (username, password, nama_lengkap, email, no_telp)
                VALUES (?, ?, ?, ?, ?)
            """, (username, hash_password(password), nama_lengkap, email, no_telp))
            conn.commit()

        flash("Registrasi berhasil, silakan login.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user_role') != 'admin':
        flash("Harus login sebagai admin.")
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', username=session.get('user_username'))

@app.route('/pelamar/dashboard')
def pelamar_dashboard():
    if session.get('user_role') != 'pelamar':
        flash("Harus login sebagai pelamar.")
        return redirect(url_for('login'))
    
    # dummy lowongan sementara
    return render_template('pelamar_dashboard.html', username=session.get('user_username'), lowongan=[])
@app.route('/admin/tambah-lowongan', methods=['GET', 'POST'])
def tambah_lowongan():
    if session.get('user_role') != 'admin':
        flash("Harus login sebagai admin.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        nama_posisi = request.form['nama_posisi']
        deskripsi = request.form['deskripsi']
        batas_akhir = request.form['batas_akhir']
        informasi_pribadi = request.form.getlist('informasi_pribadi[]')

        data_kriteria_json = request.form['data_kriteria']
        data_kriteria = json.loads(data_kriteria_json)

        print("Nama posisi:", nama_posisi)
        print("Batas akhir:", batas_akhir)
        print("Deskripsi:", deskripsi)
        print("Informasi pribadi:", informasi_pribadi)
        print("Data Kriteria Terstruktur:")
        print(json.dumps(data_kriteria, indent=2))

        flash("Lowongan berhasil ditambahkan (simulasi).")
        return redirect(url_for('admin_dashboard'))

    return render_template('tambah_lowongan.html')


@app.route('/admin/statistik')
def admin_statistik():
    if session.get('user_role') != 'admin':
        flash("Harus login sebagai admin.")
        return redirect(url_for('login'))
    return render_template('statistik_pelamar.html')  # file HTML statistik

@app.route('/admin/laporan')
def admin_laporan():
    if session.get('user_role') != 'admin':
        flash("Harus login sebagai admin.")
        return redirect(url_for('login'))
    return render_template('laporan_analisa.html')  # file HTML laporan

@app.route('/logout')
def logout():
    session.clear()
    flash("Berhasil logout.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))  # ambil port dari Glitch, default 5000
    app.run(host='0.0.0.0', port=port, debug=True)
