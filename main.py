import sqlite3
import tkinter as tk
from tkinter import messagebox


# Veritabanı bağlantısını oluşturma ve tabloları oluşturma
def veritabani_baglantisi():
    conn = sqlite3.connect('yaz_okulu.db')
    cursor = conn.cursor()

    # Öğrenci tablosunu oluşturma
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ogrenci (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            kredi_siniri INTEGER NOT NULL,
            odeme_durumu INTEGER NOT NULL
        )
    ''')

    # Ders tablosunu oluşturma
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            kredi INTEGER NOT NULL,
            kontenjan INTEGER NOT NULL,
            hoca TEXT NOT NULL
        )
    ''')

    # Öğrenci-Ders ilişki tablosunu oluşturma
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ogrenci_ders (
            ogrenci_id INTEGER,
            ders_id INTEGER,
            FOREIGN KEY (ogrenci_id) REFERENCES ogrenci(id),
            FOREIGN KEY (ders_id) REFERENCES ders(id)
        )
    ''')

    conn.commit()
    return conn, cursor


# Öğrenci ekleme fonksiyonu
def veritabani_ogrenci_ekle(cursor, ad, kredi_siniri, odeme_durumu):
    cursor.execute('''
        INSERT INTO ogrenci (ad, kredi_siniri, odeme_durumu) 
        VALUES (?, ?, ?)
    ''', (ad, kredi_siniri, odeme_durumu))
    cursor.connection.commit()


# Ders ekleme fonksiyonu
def veritabani_ders_ekle(cursor, ad, kredi, kontenjan, hoca):
    cursor.execute('''
        INSERT INTO ders (ad, kredi, kontenjan, hoca) 
        VALUES (?, ?, ?, ?)
    ''', (ad, kredi, kontenjan, hoca))
    cursor.connection.commit()


# Öğrenci-Ders kaydı ekleme fonksiyonu
def veritabani_ogrenci_ders_ekle(cursor, ogrenci_id, ders_id):
    cursor.execute('''
        INSERT INTO ogrenci_ders (ogrenci_id, ders_id) 
        VALUES (?, ?)
    ''', (ogrenci_id, ders_id))
    cursor.connection.commit()


# Öğrenci listesini alma fonksiyonu
def veritabani_ogrenci_listesi(cursor):
    cursor.execute('SELECT * FROM ogrenci')
    return cursor.fetchall()


# Ders listesini alma fonksiyonu
def veritabani_ders_listesi(cursor):
    cursor.execute('SELECT * FROM ders')
    return cursor.fetchall()


# Belirli bir öğrencinin aldığı dersleri alma fonksiyonu
def veritabani_ogrencinin_aldigi_dersler(cursor, ogrenci_id):
    cursor.execute('''
        SELECT ders.ad, ders.kredi 
        FROM ders 
        JOIN ogrenci_ders ON ders.id = ogrenci_ders.ders_id 
        WHERE ogrenci_ders.ogrenci_id = ?
    ''', (ogrenci_id,))
    return cursor.fetchall()


# Öğrenci silme fonksiyonu
def veritabani_ogrenci_sil(cursor, ogrenci_id):
    # Öğrencinin kayıtlı olduğu derslerden silinmesi
    cursor.execute('DELETE FROM ogrenci_ders WHERE ogrenci_id = ?', (ogrenci_id,))
    # Öğrencinin silinmesi
    cursor.execute('DELETE FROM ogrenci WHERE id = ?', (ogrenci_id,))
    cursor.connection.commit()


# Ders silme fonksiyonu
def veritabani_ders_sil(cursor, ders_id):
    # Derse kayıtlı öğrencilerin ilişkisinin silinmesi
    cursor.execute('DELETE FROM ogrenci_ders WHERE ders_id = ?', (ders_id,))
    # Dersin silinmesi
    cursor.execute('DELETE FROM ders WHERE id = ?', (ders_id,))
    cursor.connection.commit()


# GUI işlevleri
def ogrenci_ekle_gui(cursor):
    def ekle():
        ad = ad_entry.get()
        kredi_siniri = int(kredi_entry.get())
        odeme_durumu = 1 if odeme_var.get() == 1 else 0
        veritabani_ogrenci_ekle(cursor, ad, kredi_siniri, odeme_durumu)
        messagebox.showinfo("Başarılı", f"{ad} adlı öğrenci başarıyla eklendi.")
        ekle_penceresi.destroy()

    ekle_penceresi = tk.Toplevel()
    ekle_penceresi.title("Öğrenci Ekle")
    tk.Label(ekle_penceresi, text="Ad:").grid(row=0, column=0)
    ad_entry = tk.Entry(ekle_penceresi)
    ad_entry.grid(row=0, column=1)
    tk.Label(ekle_penceresi, text="Kredi Sınırı:").grid(row=1, column=0)
    kredi_entry = tk.Entry(ekle_penceresi)
    kredi_entry.grid(row=1, column=1)
    tk.Label(ekle_penceresi, text="Ödeme Durumu:").grid(row=2, column=0)
    odeme_var = tk.IntVar()
    tk.Checkbutton(ekle_penceresi, text="Ödendi", variable=odeme_var).grid(row=2, column=1)
    tk.Button(ekle_penceresi, text="Ekle", command=ekle).grid(row=3, column=0, columnspan=2)


def ders_ekle_gui(cursor):
    def ekle():
        ad = ad_entry.get()
        kredi = int(kredi_entry.get())
        kontenjan = int(kontenjan_entry.get())
        hoca = hoca_entry.get()
        veritabani_ders_ekle(cursor, ad, kredi, kontenjan, hoca)
        messagebox.showinfo("Başarılı", f"{ad} adlı ders başarıyla eklendi.")
        ekle_penceresi.destroy()

    ekle_penceresi = tk.Toplevel()
    ekle_penceresi.title("Ders Ekle")
    tk.Label(ekle_penceresi, text="Ders Adı:").grid(row=0, column=0)
    ad_entry = tk.Entry(ekle_penceresi)
    ad_entry.grid(row=0, column=1)
    tk.Label(ekle_penceresi, text="Kredi:").grid(row=1, column=0)
    kredi_entry = tk.Entry(ekle_penceresi)
    kredi_entry.grid(row=1, column=1)
    tk.Label(ekle_penceresi, text="Kontenjan:").grid(row=2, column=0)
    kontenjan_entry = tk.Entry(ekle_penceresi)
    kontenjan_entry.grid(row=2, column=1)
    tk.Label(ekle_penceresi, text="Hoca:").grid(row=3, column=0)
    hoca_entry = tk.Entry(ekle_penceresi)
    hoca_entry.grid(row=3, column=1)
    tk.Button(ekle_penceresi, text="Ekle", command=ekle).grid(row=4, column=0, columnspan=2)


def ogrenci_sil_gui(cursor):
    def sil():
        ad = ad_entry.get()
        cursor.execute('SELECT id FROM ogrenci WHERE ad = ?', (ad,))
        ogrenci = cursor.fetchone()
        if ogrenci:
            veritabani_ogrenci_sil(cursor, ogrenci[0])
            messagebox.showinfo("Başarılı", f"{ad} adlı öğrenci başarıyla silindi.")
            sil_penceresi.destroy()
        else:
            messagebox.showerror("Hata", "Öğrenci bulunamadı.")

    sil_penceresi = tk.Toplevel()
    sil_penceresi.title("Öğrenci Sil")
    tk.Label(sil_penceresi, text="Öğrenci Adı:").grid(row=0, column=0)
    ad_entry = tk.Entry(sil_penceresi)
    ad_entry.grid(row=0, column=1)
    tk.Button(sil_penceresi, text="Sil", command=sil).grid(row=1, column=0, columnspan=2)


def ders_sil_gui(cursor):
    def sil():
        ad = ad_entry.get()
        cursor.execute('SELECT id FROM ders WHERE ad = ?', (ad,))
        ders = cursor.fetchone()
        if ders:
            veritabani_ders_sil(cursor, ders[0])
            messagebox.showinfo("Başarılı", f"{ad} adlı ders başarıyla silindi.")
            sil_penceresi.destroy()
        else:
            messagebox.showerror("Hata", "Ders bulunamadı.")

    sil_penceresi = tk.Toplevel()
    sil_penceresi.title("Ders Sil")
    tk.Label(sil_penceresi, text="Ders Adı:").grid(row=0, column=0)
    ad_entry = tk.Entry(sil_penceresi)
    ad_entry.grid(row=0, column=1)
    tk.Button(sil_penceresi, text="Sil", command=sil).grid(row=1, column=0, columnspan=2)


def ogrenci_listesi_gui(cursor):
    liste_penceresi = tk.Toplevel()
    liste_penceresi.title("Öğrenci Listesi")

    ogrenciler = veritabani_ogrenci_listesi(cursor)

    row = 0
    for ogrenci in ogrenciler:
        ogrenci_id, ad, kredi_siniri, odeme_durumu = ogrenci
        odeme_durumu_str = "Ödendi" if odeme_durumu else "Ödenmedi"
        dersler = veritabani_ogrencinin_aldigi_dersler(cursor, ogrenci_id)
        dersler_str = ", ".join([f"{ders_ad} ({kredi} kredi)" for ders_ad, kredi in dersler])

        ogrenci_frame = tk.LabelFrame(liste_penceresi, text=f"Öğrenci {ogrenci_id}", padx=10, pady=10)
        ogrenci_frame.grid(row=row, column=0, padx=10, pady=10, sticky="w")

        tk.Label(ogrenci_frame, text=f"Ad: {ad}").grid(row=0, column=0, sticky="w")
        tk.Label(ogrenci_frame, text=f"Kredi Sınırı: {kredi_siniri}").grid(row=1, column=0, sticky="w")
        tk.Label(ogrenci_frame, text=f"Ödeme Durumu: {odeme_durumu_str}").grid(row=2, column=0, sticky="w")
        tk.Label(ogrenci_frame, text=f"Aldığı Dersler: {dersler_str}").grid(row=3, column=0, sticky="w")

        row += 1


def ders_listesi_gui(cursor):
    liste_penceresi = tk.Toplevel()
    liste_penceresi.title("Ders Listesi")

    dersler = veritabani_ders_listesi(cursor)

    row = 0
    for ders in dersler:
        ders_id, ad, kredi, kontenjan, hoca = ders

        ders_frame = tk.LabelFrame(liste_penceresi, text=f"Ders {ders_id}", padx=10, pady=10)
        ders_frame.grid(row=row, column=0, padx=10, pady=10, sticky="w")

        tk.Label(ders_frame, text=f"Ders Adı: {ad}").grid(row=0, column=0, sticky="w")
        tk.Label(ders_frame, text=f"Kredi: {kredi}").grid(row=1, column=0, sticky="w")
        tk.Label(ders_frame, text=f"Kontenjan: {kontenjan}").grid(row=2, column=0, sticky="w")
        tk.Label(ders_frame, text=f"Hoca: {hoca}").grid(row=3, column=0, sticky="w")

        row += 1


# Ana program
def main():
    conn, cursor = veritabani_baglantisi()

    # Ana pencere
    root = tk.Tk()
    root.title("Yaz Okulu Kayıt Sistemi")

    tk.Button(root, text="Öğrenci Ekle", command=lambda: ogrenci_ekle_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Ders Ekle", command=lambda: ders_ekle_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Öğrenci Sil", command=lambda: ogrenci_sil_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Ders Sil", command=lambda: ders_sil_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Öğrencileri Listele", command=lambda: ogrenci_listesi_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Dersleri Listele", command=lambda: ders_listesi_gui(cursor)).pack(pady=5)
    tk.Button(root, text="Çıkış", command=root.quit).pack(pady=5)

    root.mainloop()
    conn.close()


if __name__ == "__main__":
    main()
