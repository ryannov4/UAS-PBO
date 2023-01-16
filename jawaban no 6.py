import mysql.connector

mydb = mysql.connector.connect(
  host="172.29.175.81",
  port=23306,
  user="root",
  password="p455w0rd",
)

if mydb.is_connected():
  print("Berhasil terhubung ke database")