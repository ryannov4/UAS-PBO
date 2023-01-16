#-------------------------------------------------------------------------------
# Name:        File 1 - CRUD Mahasiswa
# Purpose:     Just for fun
#
# Author:      Dendi Nasrulloh
#
# Created:     01/10/2022
# Copyright:   (c) Dendi Nasrulloh
# Licence:     Open Source
#-------------------------------------------------------------------------------

import mysql.connector
import os
import hashlib
from prettytable import PrettyTable


db = mysql.connector.connect(host="localhost", user="root", password="", database="db_nilaimhs")

# membuat fungsi untuk insert data mahasiswa
def insert_data_mhs(db):
    print("===================================")
    print("      INPUT DATA MAHASISWA         ")
    print("===================================")
    nim = int(input("Masukkan NIM: "))
    cursor = db.cursor()
    cekdulu = "SELECT nim_mhs FROM tbl_mhs WHERE nim_mhs=%s"
    val = (nim, )
    cursor.execute(cekdulu, val)
    hasilcekna = cursor.fetchall()
    if cursor.rowcount > 0:
        print("NIM. {} sudah terdaftar di database!".format(nim))
    else:
        nama = input("Nama Mahasiswa: ")
        namana = nama.upper()
        kelas = input("Kelas: ")
        kelasna = kelas.upper()
        jurusan = input("Jurusan: ")
        jurusana = jurusan.upper()
        val2 = (nim, namana, kelasna, jurusana)
        sql = "INSERT INTO tbl_mhs (nim_mhs, nama_mhs, kelas_mhs, jurusan_mhs) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, val2)
        db.commit()
        print("Data Mahasiswa Berhasil disimpan!")

# membuat fungsi untuk insert data nilai mata kuliah
def insert_data_nilai(db):
    print("===================================")
    print("      INPUT NILAI MAHASISWA        ")
    print("===================================")
    cursor = db.cursor()
    nim = int(input("Masukkan NIM: "))
    cekdata = "SELECT nim_mhs FROM tbl_mhs WHERE nim_mhs=%s"
    valcek = (nim, )
    cursor.execute(cekdata, valcek)
    hasilcek = cursor.fetchall()
    if cursor.rowcount < 1:
        print("Belum ada mahasiswa dengan NIM. {} di dalam database!".format(nim))
    else:
        namaMatkul = input("Mata Kuliah: ")
        makul = namaMatkul.upper()
        valcekm = (makul, nim)
        cekmakul = "SELECT nama_matakuliah FROM tbl_nilai WHERE nama_matakuliah=%s AND nim_mhs=%s"
        cursor.execute(cekmakul, valcekm)
        hasilcekm = cursor.fetchall()
        if cursor.rowcount > 0:
            print("Mata kuliah ini sudah ada dalam database!")
        else:
            sks = int(input("Bobot SKS (angka): "))
            nilai = input("Nilai Mata Kuliah (huruf): ")
            nil = nilai.upper()
            smt = int(input("Semester (angka): "))
            # cek semester ganjil atau genap
            if smt % 2 == 0 :
                periode = "GENAP"
            else:
                periode = "GANJIL"
            dosen = input("Nama Dosen: ")
            dosenUp = dosen.upper()
            val = (nim, makul, sks, nil, smt, periode, dosenUp)
            cursor = db.cursor()
            sql = "INSERT INTO tbl_nilai (nim_mhs, nama_matakuliah, sks_matakuliah, nilai_mhs, semester, periode, nm_dosen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, val)
            db.commit()
            print("Data Nilai Berhasil disimpan!")

# fungsi untuk menampilkan data (SELECT)
def tampil_data(db):
    print("===================================")
    print("    TAMPILKAN DATA MAHASISWA       ")
    print("===================================")
    nim = int(input("Masukkan NIM: "))
    cursor = db.cursor(dictionary=True)
    val = (nim, )
    sql = "SELECT * FROM tbl_mhs WHERE nim_mhs=%s"
    cursor.execute(sql, val)
    hasil = cursor.fetchall()

    if cursor.rowcount < 1:
        print("Data mahasiswa tidak ditemukan")
    else:
        print("\n=====================================")
        print("      DAFTAR NILAI MATA KULIAH")
        print("=====================================")
        for i in hasil:
            print("NIM\t\t: " + i['nim_mhs'])
            print("Nama\t\t: " + i['nama_mhs'])
            print("Kelas\t\t: " + i['kelas_mhs'])
            print("Jurusan\t\t: " + i['jurusan_mhs'])
            print("\n")

    sql2 = "SELECT * FROM tbl_nilai WHERE nim_mhs=%s ORDER BY semester ASC"
    cursor.execute(sql2, val)
    hasil2 = cursor.fetchall()
    noUrut = 1
    jumNilai = 0
    sksAwal = 0

    if cursor.rowcount < 1:
        print("Belum ada data nilai untuk mahasiswa dengan NIM. {}!".format(nim))
    else:
        tabel = PrettyTable()
        tabel.field_names = ["NO", "MATA KULIAH", "SKS", "NILAI", "SEMESTER", "PERIODE", "NAMA DOSEN"]
        for n in hasil2:
            tabel.add_row([noUrut, n['nama_matakuliah'], n['sks_matakuliah'], n['nilai_mhs'], n['semester'], n['periode'], n['nm_dosen']])
            if n['nilai_mhs'] == "A":
                nilnil = 4
            elif n['nilai_mhs'] == "B":
                nilnil = 3
            elif n['nilai_mhs'] == "C":
                nilnil = 2
            elif n['nilai_mhs'] == "D":
                nilnil = 1
            else:
                nilnil = 0
            nilaiMatkul = n['sks_matakuliah'] * nilnil
            jumNilai += nilaiMatkul
            sksAwal += n['sks_matakuliah']
            noUrut += 1
        tabel.align["MATA KULIAH"] = "l"
        tabel.align["NAMA DOSEN"] = "l"
        print(tabel)
        tabel.clear_rows()
        print("Total Nilai \t: ", jumNilai)
        ip = jumNilai / sksAwal
        ipNa = float(round(ip,2))
        print("IPK \t\t: ", ipNa)
        # kondisi untuk keterangan IPK
        if ipNa > 3.75:
            ketIp = "Sangat Baik"
        elif ipNa <= 3.75 and ipNa > 3.00:
            ketIp = "Baik"
        elif ipNa <= 3.00 and ipNa > 2.85:
            ketIp = "Cukup"
        else:
            ketIp = "Kurang"
        print("Keterangan \t: ", ketIp)


# fungsi untuk merubah data (UPDATE) mahasiswa
def ubah_data_mhs(db):
    print("===================================")
    print("         UBAH DATA MAHASISWA       ")
    print("===================================")
    cursor = db.cursor(dictionary=True)
    nim = int(input("Masukkan NIM: "))
    cekdata = "SELECT nim_mhs FROM tbl_mhs WHERE nim_mhs=%s"
    valcek = (nim, )
    cursor.execute(cekdata, valcek)
    hasilcek = cursor.fetchall()
    if cursor.rowcount < 1:
        print("Data Mahasiswa tidak ditemukan!")
    else:
        nama = input("Nama Mahasiswa: ")
        namana = nama.upper()
        kelas = input("Kelas: ")
        kelasna = kelas.upper()
        jurusan = input("Jurusan: ")
        jurusana = jurusan.upper()

        sql = "UPDATE tbl_mhs SET nama_mhs=%s, kelas_mhs=%s, jurusan_mhs=%s WHERE nim_mhs=%s"
        val = (namana, kelasna, jurusana, nim)
        cursor.execute(sql, val)
        db.commit()
        print("Data mahasiswa an. {} dengan NIM. {} berhasil dirubah.".format(namana, nim))

# fungsi untuk merubah data (UPDATE) nilai mahasiswa
def ubah_data_nilai(db):
    print("===================================")
    print("         UBAH DATA NILAI           ")
    print("===================================")
    cursor = db.cursor(dictionary=True)
    nim = int(input("Masukkan NIM: "))
    cekdata = "SELECT nim_mhs FROM tbl_nilai WHERE nim_mhs=%s"
    valcek = (nim, )
    cursor.execute(cekdata, valcek)
    hasilcek = cursor.fetchall()
    if cursor.rowcount < 1:
        print("Belum ada data nilai untuk mahasiswa dengan NIM. {}!".format(nim))
    else:
        matakul = input("Mata Kuliah: ")
        matKul = matakul.upper()
        cekmatakul = "SELECT nama_matakuliah FROM tbl_nilai WHERE nama_matakuliah=%s AND nim_mhs=%s"
        valmatkul = (matKul, nim)
        cursor.execute(cekmatakul, valmatkul)
        hasilcekmatakul = cursor.fetchall()
        if cursor.rowcount < 1:
            print("Belum ada data nilai untuk mata kuliah {}!".format(matKul))
        else:
            sksbaru = int(input("Bobot SKS (angka): "))
            nilaibaru = input("Nilai Mata Kuliah (huruf): ")
            nilbar = nilaibaru.upper()
            sql = "UPDATE tbl_nilai SET sks_matakuliah=%s, nilai_mhs=%s WHERE nim_mhs=%s AND nama_matakuliah=%s"
            val = (sksbaru, nilbar, nim, matKul)
            cursor.execute(sql, val)
            db.commit()
            print("Data nilai mahasiswa dengan NIM. {} pada mata kuliah {} berhasil dirubah.".format(nim, matKul))

# fungsi untuk menghapus data mahasiswa beserta nilainya (DELETE)
def delete_data(db):
    print("===================================")
    print("         HAPUS DATA MAHASISWA      ")
    print("===================================")
    cursor = db.cursor()
    nim = int(input("Masukkan NIM: "))
    val = (nim, )
    cekdulu = "SELECT tbl_mhs.nim_mhs, tbl_nilai.nim_mhs FROM tbl_mhs LEFT JOIN tbl_nilai ON tbl_mhs.nim_mhs=tbl_nilai.nim_mhs WHERE tbl_mhs.nim_mhs=%s"
    cursor.execute(cekdulu, val)
    hasilcekna = cursor.fetchall()
    if cursor.rowcount < 1:
        print("Tidak ditemukan mahasiswa dengan NIM. {}".format(nim))
    else:
        sql = "DELETE tbl_mhs, tbl_nilai FROM tbl_mhs LEFT JOIN tbl_nilai ON tbl_mhs.nim_mhs=tbl_nilai.nim_mhs WHERE tbl_mhs.nim_mhs=%s"
        cursor.execute(sql, val)
        db.commit()
        print("Data mahasiswa dengan NIM. {} berhasil dihapus!".format(nim))

# fungsi untuk menghapus nilai mahasiswa (DELETE)
def delete_nilai(db):
    print("===================================")
    print("       HAPUS NILAI MAHASISWA       ")
    print("===================================")
    cursor = db.cursor()
    nim = int(input("Masukkan NIM: "))
    val = (nim, )
    cekdulu = "SELECT nim_mhs FROM tbl_nilai WHERE nim_mhs=%s"
    cursor.execute(cekdulu, val)
    hasilcekna = cursor.fetchall()
    if cursor.rowcount < 1:
        print("Belum ada data nilai untuk mahasiswa dengan NIM. {}".format(nim))
    else:
        makul = input("Mata Kuliah yang akan dihapus: ")
        matkul = makul.upper()
        cekmakul = "SELECT nama_matakuliah FROM tbl_nilai WHERE nama_matakuliah=%s AND nim_mhs=%s"
        val2 = (matkul, nim)
        cursor.execute(cekmakul, val2)
        hasilcekmakul = cursor.fetchall()
        if cursor.rowcount < 1:
            print("Belum ada data nilai matakuliah {} untuk mahasiswa dengan NIM {}".format(matkul, nim))
        else:
            sqlna = "DELETE FROM tbl_nilai WHERE nama_matakuliah=%s AND nim_mhs=%s"
            cursor.execute(sqlna, val2)
            db.commit()
            print("Mata kuliah {} telah dihapus untuk mahasiswa dengan NIM. {}".format(matkul, nim))

# fungsi untuk mencari data
def cari_data(db):
    print("===================================")
    print("       CARI DATA MAHASISWA         ")
    print("===================================")
    keyword = input("Masukkan keyword: ")
    cursor = db.cursor(dictionary=True)
    cekmhs = "SELECT * FROM tbl_mhs WHERE nama_mhs LIKE %s OR kelas_mhs LIKE %s OR jurusan_mhs LIKE %s"
    val = ("%{}%".format(keyword), "%{}%".format(keyword), "%{}%".format(keyword))
    cursor.execute(cekmhs, val)
    hasilna = cursor.fetchall()
    noUrut = 1
    if cursor.rowcount < 1:
        print("Tidak ditemukan data dengan keyword {}".format(keyword))
    else:
        print("\nHASIL PENCARIAN DATA DENGAN KEYWORD : {}".format(keyword))
        print("Ditemukan {} data\n".format(cursor.rowcount))
        tabel2 = PrettyTable()
        tabel2.field_names = ["NO", "NIM", "NAMA MAHASISWA", "KELAS", "JURUSAN"]
        for i in hasilna:
            tabel2.add_row([noUrut, i['nim_mhs'], i['nama_mhs'], i['kelas_mhs'], i['jurusan_mhs']])
            noUrut += 1
        tabel2.align["NAMA MAHASISWA"] = "l"
        tabel2.align["JURUSAN"] = "l"
        print(tabel2)
        tabel2.clear_rows()

# fungsi untuk login
def login_aplikasi(db):
    print("===================================")
    print("   LOGIN APLIKASI DATA MAHASISWA   ")
    print("===================================")
    username = input("Username: ")
    password = input("Password: ")
    pwd = hashlib.md5(password.encode())
    pwdna = pwd.hexdigest()

    cursor = db.cursor()
    sql = "SELECT * FROM tbl_user WHERE username=%s AND password=%s"
    val = (username, pwdna)
    cursor.execute(sql, val)
    hasil = cursor.fetchall()

    if cursor.rowcount > 0:
        os.system("cls")
        print("\nHallo {}, anda berhasil login. Silahkan pilih menu!".format(username))
        while True:
            tampil_menu(db)
    else:
        print("Username atau Password tidak ditemukan!\n")
        login_aplikasi(db)

# membuat fungsi memilih menu
def tampil_menu(db):
    print("\n===================================")
    print("      APLIKASI DATA MAHASISWA       ")
    print("===================================")
    print("1. Input Data Mahasiswa")
    print("2. Input Data Nilai")
    print("3. Tampilkan Data")
    print("4. Ubah Data Mahasiswa")
    print("5. Ubah Data Nilai")
    print("6. Hapus Data")
    print("7. Hapus Nilai Mata Kuliah")
    print("8. Cari Data")
    print("0. Keluar")
    print("--------------------------------")
    menu = input("Pilih Menu: ")

    # bersihkan layar
    os.system("cls")

    # membuat pilihan menu
    if menu == "1":
        insert_data_mhs(db)
    elif menu == "2":
        insert_data_nilai(db)
    elif menu == "3":
        tampil_data(db)
    elif menu == "4":
        ubah_data_mhs(db)
    elif menu == "5":
        ubah_data_nilai(db)
    elif menu == "6":
        delete_data(db)
    elif menu == "7":
        delete_nilai(db)
    elif menu == "8":
        cari_data(db)
    elif menu == "0":
        print("Terima kasih, anda telah keluar dari aplikasi!")
        exit()
    else:
        print("Tidak ditemukan menu {} di program ini!".format(menu))

if __name__ == "__main__":
    login_aplikasi(db)




