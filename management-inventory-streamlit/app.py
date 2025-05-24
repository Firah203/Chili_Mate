import streamlit as st
import pandas as pd
from db_manager import add_item, get_all_items, decrease_item_stock, create_table
from search import search_item 


# Membuat Tabel jika belum ada
create_table()  

# Fungsi untuk menampilkan data dari database
def load_data():
    rows = get_all_items()
    return pd.DataFrame(rows, columns=["Kode Barang", "Nama Barang", "Stok", "Harga per Unit"])

# Halaman Utama
st.title("Chili Mate 🌶️", page_icon="🌶️")

# Pencarian Barang
st.subheader("Pencarian Barang")
search_keyword = st.text_input("Cari berdasarkan kode barang atau nama barang:") 
if search_keyword:  
    search_results = search_item(search_keyword)
    if search_results:
        df = pd.DataFrame(search_results, columns=["Kode Barang", "Nama Barang", "Stok", "Harga per Unit"])
        st.dataframe(df)
    else:
        st.warning("Barang tidak ditemukan.")                
else: 
     # Tampilkan semua barang jika tidak ada pencarian
     st.subheader("Inventaris Saat Ini")    
     df = load_data()
     st.datadataframe(df)

# Tampilkan data inventaris
st.subheader("Inventaris Saat Ini")
bf = load_data()
st.dataframe(df)

# Barang Keluar(Pengurangan Stok)
st.subheader("Barang Keluar")
with st.form("Barang Keluar"):
    kode_barang = st.text_input("Kode Barang") # Menggunakan Kode Barang
    quantity = st.number_input("Jumlah Barang Keluar", min_value=1, step=1)
    submit = st.form_submit_button("Proses Barang Keluar")

    if submit:
        if kode_barang and quantity > 0:
            # Panggil fungsi untuk mengurangi stok berdasarkan kode barang
            decrease_item_stock(kode_barang, quantity)
            st.success(f"Barang dengan kode {kode_barang} berhasil dikeluarkan!")
            st.rerun()  # Reload data setelah pengurangan stok
        else:
            st.error("Mohon isi kode barang dan jumlah barang keluar dengan benar.")         

# Tambah Barang Baru
st.subheader("Tambah Barang Baru")
with st.form("Tambah Barang"):
    kode_barang = st.text_input("Kode Barang")
    nama_barang = st.text_input("Nama Barang")
    stok = st.number_input("Stok", min_value=0, step=1)
    harga = st.number_input("Harga", min_value=0.0, step=100)
    submit = st.form_submit_button("Tambah")

    if submit:
        # Tambah data ke database
        if kode_barang and nama_barang and stok > 0 and harga > 0:
            add_item(kode_barang, nama_barang, stok, harga) 
            st.success("Barang berhasil ditambahkan!")
            st.rerun() # Reload data setelah penambahan barang
        else: 
            st.error("Mohon isi semua data dengan benar")

# Export Data
st.subheader("Unduh Data Inventaris")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data CSV",
    data=csv,
    file_name='inventaris.csv',
    mime='text/csv')




                                                                 

                              