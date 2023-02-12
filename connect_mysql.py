import mysql.connector

# koneksi ke dbms
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    database = 'pythondasar',
    password = ''
)

# membuat tempat untuk eksekusi sql
querybox = conn.cursor()

# membuat database
# querybox.execute("CREATE DATABASE pythondasar")
# setelah dimasukan harus ditambahkan ke conn diatas

# membuat table (pakai ''' agar bisa dienter)
querybox.execute("create table if not exists family(id int AUTO_INCREMENT PRIMARY KEY,"
    "name varchar(30) not null,"
    "age int(3),"
    "status varchar(30))")
conn.commit()

# mengisi tabel dengan data
nama = "Rizky Radityo"
usia = 31
posisi = "Kepala Keluarga"
query = "INSERT INTO family(name,age,status) VALUES(%s,%s,%s)"
value = (nama,usia,posisi)
querybox.execute(query,value)
conn.commit()