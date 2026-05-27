import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import base64
import urllib.parse

# Konfigurasi Halaman
st.set_page_config(
    page_title="Satsun Coffee",
    page_icon="☕",
    layout="centered"
)

# Nama file database Excel dan Folder Gambar
EXCEL_FILE = "menu.xlsx"
IMAGE_FOLDER = "assets"
NOMOR_WHATSAPP = "6281335303199" # Nomor WhatsApp Satsun

# Membuat folder assets secara otomatis jika belum ada
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# --- FUNGSI BARU: KONVERSI GAMBAR LOKAL KE BASE64 AGAR MUNCUL DI HTML ---
def get_image_base64(path_gambar):
    try:
        with open(path_gambar, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            # Otomatis menentukan mime type berdasarkan ekstensi
            ext = os.path.splitext(path_gambar)[1].lower()
            mime_type = "image/png" if ext == ".png" else "image/jpeg"
            return f"data:{mime_type};base64,{encoded_string}"
    except Exception:
        return None

# --- FUNGSI UNTUK MANAJEMEN DATA EXCEL ---
def load_data():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        if "Gambar" not in df.columns:
            df["Gambar"] = ""
            df.to_excel(EXCEL_FILE, index=False)
        return df
    else:
        data = {
            "Kategori": ["Coffee", "Coffee", "Non-Coffee", "Snack"],
            "Nama Menu": ["Satsun Signature Latte", "Espresso", "Matcha Latte", "Croissant Butter"],
            "Harga": [28000, 18000, 25000, 22000],
            "Gambar": ["", "", "", ""]
        }
        df = pd.DataFrame(data)
        df.to_excel(EXCEL_FILE, index=False)
        return df

def save_data(df):
    df.to_excel(EXCEL_FILE, index=False)

# Load data menu
df_menu = load_data()

# --- INISIALISASI MEMORI KERANJANG (SESSION STATE) ---
if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- KUSTOMISASI WARNA (LATTE & COFFEE NUANCE) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    
    h1, h2, h3, p, span, label { 
        color: #3E2723 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .menu-card {
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #8D6E63; 
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 5px;
    }
    
    .stButton>button { 
        background-color: #D7CCC8 !important; 
        color: #3E2723 !important;            
        border-radius: 8px !important;
        border: 1px solid #BCAAA4 !important;
        font-weight: bold !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background-color: #BCAAA4 !important; 
        color: #3E2723 !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton>button[data-testid="baseButton-primary"] {
        background-color: #FFCDD2 !important;
        color: #B71C1C !important;
        border: 1px solid #EF9A9A !important;
    }
    .stButton>button[data-testid="baseButton-primary"]:hover {
        background-color: #E57373 !important;
        color: #FFFFFF !important;
    }
    
    hr { border: 0; height: 1px; background: #E0D4C3; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- NAVIGASI MENU ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Our Menu & Orders", "Find Us", "Admin Dashboard"],
    icons=["house-fill", "cup-hot-fill", "geo-alt-fill", "speedometer2"],
    default_index=0,  # <-- Cukup ubah angka ini dari 1 menjadi 0
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#EFEBE9 !important", "border-radius": "8px", "border": "1px solid #D7CCC8"},
        "icon": {"color": "#5D4037 !important", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin": "0px", "color": "#5D4037 !important", "font-weight": "600", "background-color": "transparent"},
        "nav-link-selected": {"background-color": "#5D4037 !important", "color": "#FFFFFF !important", "font-weight": "bold", "border-radius": "6px"},
    }
)

if selected == "Home":
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>☕ Welcome to Satsun Coffee</h1>", unsafe_allow_html=True)
    if os.path.exists("foto_cafe.jpg"):
        st.image("foto_cafe.jpg", use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=800", use_container_width=True)
    st.markdown("<h3 style='text-align: center; color: #6D4C41;'>Where Every Sip Tells a Story</h3>", unsafe_allow_html=True)
    st.write("Satsun Coffee hadir untuk menemani hari Anda dengan racikan kopi pilihan.")
    
elif selected == "Our Menu & Orders":
    st.title("📋 Menu Satsun")
    
    col_menu, col_cart = st.columns([5, 3])
    
    with col_menu:
        kategori_opsi = ["Semua"] + list(df_menu["Kategori"].unique())
        kategori = st.selectbox("Filter Kategori:", kategori_opsi)
        
        if kategori == "Semua":
            df_filtered = df_menu
        else:
            df_filtered = df_menu[df_menu["Kategori"] == kategori]
            
        st.write("") 
        
        if df_filtered.empty:
            st.warning("Belum ada menu di kategori ini.")
        else:
            for index, row in df_filtered.iterrows():
                nama_item = row['Nama Menu']
                harga_item = row['Harga']
                kat_item = row['Kategori']
                nama_gambar = row['Gambar'] if 'Gambar' in row and pd.notna(row['Gambar']) else ""
                
                # Resolusi path gambar menggunakan Base64 encoder
                path_gambar_penuh = os.path.join(IMAGE_FOLDER, str(nama_gambar))
                src_gambar = None
                
                if nama_gambar != "" and os.path.exists(path_gambar_penuh):
                    src_gambar = get_image_base64(path_gambar_penuh)
                
                # Jika file tidak ditemukan atau kosong, pakai placeholder gambar kopi default
                if not src_gambar:
                    src_gambar = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=150"
                
                # Tampilan Menu Card
                st.markdown(f"""
                    <div class='menu-card'>
                        <table style='width:100%; border:none; background:transparent; border-collapse: collapse;'>
                            <tr style='background:transparent;'>
                                <td style='border:none; width:75px; padding:0px; vertical-align:middle;'>
                                    <div style='width:65px; height:65px; border-radius:8px; overflow:hidden;'>
                                        <img src='{src_gambar}' style='width:100%; height:100%; object-fit:cover;'>
                                    </div>
                                </td>
                                <td style='border:none; padding-left:12px; vertical-align:middle;'>
                                    <span style='font-weight:bold; color:#3E2723; font-size:16px;'>{nama_item}</span> <br>
                                    <span style='color:#8D6E63; font-size:12px; font-weight:normal;'>{kat_item}</span>
                                </td>
                                <td style='border:none; text-align:right; font-weight:bold; color:#5D4037; font-size:16px; vertical-align:middle;'>
                                    Rp {int(harga_item):,}
                                </td>
                            </tr>
                        </table>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"➕ Tambah {nama_item}", key=f"add_{index}"):
                    if nama_item in st.session_state.cart:
                        st.session_state.cart[nama_item] += 1
                    else:
                        st.session_state.cart[nama_item] = 1
                    st.rerun()
                    
    with col_cart:
        st.markdown("### 🛒 Keranjang")
        if not st.session_state.cart:
            st.caption("Keranjang masih kosong.")
        else:
            total_belanja = 0
            order_list_text = "" 
            for item, qty in list(st.session_state.cart.items()):
                harga = df_menu[df_menu["Nama Menu"] == item]["Harga"].values[0]
                subtotal = harga * qty
                total_belanja += subtotal
                st.markdown(f"**{item}** ({qty}x)\n👉 Rp {int(subtotal):,}")
                order_list_text += f"- {item} ({qty}x)\n"
                
            st.divider()
            st.markdown(f"#### **Total: Rp {int(total_belanja):,}**")
            nama_pelanggan = st.text_input("Nama Anda:", placeholder="Contoh: Hery")
            opsi_makan = st.radio("Metode:", ["Dine-in", "Takeaway"])
            
            if nama_pelanggan.strip() == "":
                st.button("🚀 Kirim via WhatsApp (Masukkan Nama Anda)", disabled=True)
            else:
                pesan_wa = f"Halo Satsun Coffee, saya mau pesan:\n\n{order_list_text}\nTotal Belanja: Rp {int(total_belanja):,}\nNama Pelanggan: {nama_pelanggan}\nMetode: {opsi_makan}\n\nMohon diproses ya, terima kasih! 🙏☕"
                url_wa = f"https://wa.me/{NOMOR_WHATSAPP}?text={urllib.parse.quote(pesan_wa)}"
                st.markdown(f'<a href="{url_wa}" target="_blank" style="text-decoration: none;"><div style="background-color: #D7CCC8; color: #3E2723; padding: 12px 20px; border-radius: 8px; border: 1px solid #BCAAA4; font-weight: bold; text-align: center; cursor: pointer;">🚀 Kirim via WhatsApp</div></a>', unsafe_allow_html=True)
            
            st.write("")
            if st.button("🗑️ Kosongkan", type="primary", key="clear_cart"):
                st.session_state.cart = {}
                st.rerun()

elif selected == "Find Us":
    st.title("📍 Lokasi & Kontak")
    st.write("**Alamat Kedai:** Jl. Kopi Warm No. 486")
    st.write("**Jam Operasional:** 08:00 - 22:00 WIB")
    st.write("**Kontak:** +62 813-3530-3199")
    st.markdown("- [Instagram: satsun.coffee.ins](https://www.instagram.com/satsun.coffee.ins/)")
    st.markdown("- [Facebook: satsun.coffee.fb](https://www.facebook.com/satsun.coffee.fb/)")

elif selected == "Admin Dashboard":
    st.title("📊 Satsun Internal Dashboard")
    
    st.subheader("➕ Tambah Menu Baru")
    with st.form("form_tambah_menu", clear_on_submit=True):
        new_kategori = st.selectbox("Kategori", ["Coffee", "Non-Coffee", "Snack", "Dessert"])
        new_nama = st.text_input("Nama Makanan / Minuman")
        new_harga = st.number_input("Harga (Rp)", min_value=0, step=1000)
        submit_btn = st.form_submit_button("Simpan ke Excel")
        
        if submit_btn:
            if new_nama != "":
                new_row = pd.DataFrame([{"Kategori": new_kategori, "Nama Menu": new_nama, "Harga": new_harga, "Gambar": ""}])
                df_menu = pd.concat([df_menu, new_row], ignore_index=True)
                save_data(df_menu)
                st.success("Berhasil ditambahkan! Silakan upload gambar di menu edit bawah.")
                st.rerun()
                
    st.divider()
    
    st.subheader("📝 Kelola & Edit Menu")
    st.dataframe(df_menu, use_container_width=True)
    
    col_edit, col_delete = st.columns(2)
    
    with col_edit:
        st.markdown("### ✏️ Form Edit Menu / Upload Gambar")
        menu_to_edit = st.selectbox("Pilih menu:", df_menu["Nama Menu"].unique(), key="select_edit")
        row_data = df_menu[df_menu["Nama Menu"] == menu_to_edit].iloc[0]
        
        with st.form("form_edit_menu"):
            edit_kategori = st.selectbox("Kategori Baru:", ["Coffee", "Non-Coffee", "Snack", "Dessert"], index=["Coffee", "Non-Coffee", "Snack", "Dessert"].index(row_data["Kategori"]))
            edit_nama = st.text_input("Nama Baru:", value=row_data["Nama Menu"])
            edit_harga = st.number_input("Harga Baru (Rp):", min_value=0, step=1000, value=int(row_data["Harga"]))
            uploaded_file = st.file_uploader("Upload Foto (.jpg/.jpeg/.png):", type=["jpg", "jpeg", "png"])
            save_edit_btn = st.form_submit_button("💾 Simpan Perubahan")
            
            if save_edit_btn:
                idx = df_menu[df_menu["Nama Menu"] == menu_to_edit].index[0]
                nama_file_gambar = row_data["Gambar"] if pd.notna(row_data["Gambar"]) else ""
                
                if uploaded_file is not None:
                    ext = os.path.splitext(uploaded_file.name)[1].lower()
                    nama_file_gambar = f"{edit_nama.lower().replace(' ', '_')}{ext}"
                    path_simpan = os.path.join(IMAGE_FOLDER, nama_file_gambar)
                    
                    with open(path_simpan, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                df_menu.at[idx, "Kategori"] = edit_kategori
                df_menu.at[idx, "Nama Menu"] = edit_nama
                df_menu.at[idx, "Harga"] = edit_harga
                df_menu.at[idx, "Gambar"] = nama_file_gambar
                save_data(df_menu)
                st.success("Data dan Gambar berhasil diperbarui!")
                st.rerun()

    with col_delete:
        st.markdown("### 🗑️ Hapus Menu")
        menu_to_delete = st.selectbox("Pilih menu yang ingin dihapus:", df_menu["Nama Menu"].unique(), key="select_delete")
        if st.button("❌ Hapus Menu Selected", type="primary", key="del_menu"):
            df_menu = df_menu[df_menu["Nama Menu"] != menu_to_delete]
            save_data(df_menu)
            st.error(f"'{menu_to_delete}' telah dihapus.")
            st.rerun()