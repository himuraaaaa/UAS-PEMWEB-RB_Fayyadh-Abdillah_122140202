import psycopg2
from tabulate import tabulate

# Koneksi ke database
conn = psycopg2.connect(
    dbname='barbershop_backend_db',
    user='postgres',
    password='fayyadh14',
    host='localhost',
    port=5432
)

cur = conn.cursor()

# Query data user
cur.execute("SELECT id, email, first_name, last_name, phone_number, created_at FROM users ORDER BY id DESC;")
rows = cur.fetchall()

# Tampilkan hasil
headers = ['ID', 'Email', 'First Name', 'Last Name', 'Phone Number', 'Created At']
print(tabulate(rows, headers=headers, tablefmt='psql'))

cur.close()
conn.close() 