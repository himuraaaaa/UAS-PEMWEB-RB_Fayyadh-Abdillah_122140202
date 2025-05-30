# BarberShop Management System

## Deskripsi
BarberShop Management System adalah aplikasi web yang dirancang untuk mengelola operasional barbershop secara digital. Aplikasi ini terinspirasi dari [Hairnerds Studio](https://hairnerds.id) dan menyediakan solusi manajemen untuk pemesanan layanan, pengelolaan barber, dan administrasi barbershop.

### Fitur Booking Online
Sistem ini menyediakan fitur booking online yang memungkinkan pelanggan untuk:
- Melakukan pemesanan layanan kapan saja dan di mana saja
- Memilih barber dan jadwal sesuai preferensi
- Melihat estimasi waktu layanan
- Mendapatkan konfirmasi booking secara instan
- Melacak status pemesanan secara real-time

### Manajemen Booking untuk User
Pelanggan dapat mengelola booking mereka dengan mudah:
- Melihat daftar booking aktif dan riwayat
- Melacak status booking secara real-time
- Mengedit detail booking (tanggal, waktu, layanan)
- Membatalkan booking yang belum dikonfirmasi
- Menerima notifikasi perubahan status booking
- Melihat detail layanan dan barber yang dipilih

### Keuntungan Menggunakan Sistem
1. **Bagi Pelanggan**
   - Menghemat waktu dengan pemesanan online
   - Menghindari antrian panjang
   - Fleksibilitas dalam memilih jadwal
   - Transparansi harga dan layanan
   - Riwayat layanan yang terorganisir
   - Kontrol penuh atas booking mereka
   - Kemudahan dalam mengubah atau membatalkan booking

2. **Bagi Barber**
   - Manajemen jadwal yang lebih efisien
   - Pengurangan beban administrasi
   - Peningkatan produktivitas
   - Profil profesional yang terkelola

3. **Bagi Pemilik Barbershop**
   - Peningkatan efisiensi operasional
   - Pengurangan kesalahan booking
   - Analisis data pelanggan
   - Manajemen inventori yang lebih baik
   - Peningkatan kepuasan pelanggan

## Dependensi

### Frontend (React)
```json
{
  "dependencies": {
    "@ant-design/icons": "^5.0.0",
    "antd": "^5.0.0",
    "axios": "^1.3.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "react-scripts": "5.0.1"
  }
}
```

### Backend (Python)
```txt
pyramid==2.0.2
SQLAlchemy==1.4.41
psycopg2-binary==2.9.5
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.0.1
```

## Fitur Utama
1. **Fitur Autentikasi**
   - Login pengguna
   - Registrasi pengguna baru
   - Manajemen profil pengguna
   - Reset password
   - Proteksi rute berdasarkan role

2. **Fitur Booking**
   - Pemesanan layanan secara online
   - Pemilihan barber dan jadwal
   - Konfirmasi booking
   - Riwayat pemesanan
   - Notifikasi status booking
   - Manajemen booking untuk User (edit/hapus)
   - Tracking status booking

3. **Antarmuka Pengguna**
   - Desain responsif
   - Navigasi intuitif
   - Tampilan modern dan profesional
   - Integrasi dengan sistem pembayaran

4. **Manajemen Appointment**
   - Pemesanan layanan secara online
   - Pengelolaan jadwal barber
   - Status appointment (pending, confirmed, completed, cancelled)
   - Notifikasi status appointment

5. **Manajemen Barber**
   - Profil barber dengan foto dan spesialisasi

6. **Manajemen Layanan**
   - Daftar layanan dengan harga
   - Deskripsi detail setiap layanan
   - Kategori layanan
   - Durasi estimasi layanan

7. **Manajemen Pelanggan**
   - Registrasi dan login pelanggan
   - Riwayat layanan
   - Profil pelanggan

8. **Panel Admin**
   - Dashboard dengan statistik
   - Manajemen appointment
   - Manajemen barber
   - Manajemen layanan
   - Laporan dan analitik

## Cara Menjalankan Aplikasi

### Frontend
```bash
cd barbershop_frontend
npm install
npm start
```

### Backend
```bash
cd barbershop_backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
pserve development.ini
```

## Referensi
Aplikasi ini terinspirasi dari [Hairnerds Studio](https://hairnerds.id), sebuah barbershop profesional yang menggabungkan konsep barbershop dan salon dengan fokus pada kualitas hasil potongan rambut.

## Kontributor
- Fayyadh Abdillah (122140202)

## Lisensi
MIT License 