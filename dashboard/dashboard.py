import streamlit as st
import pandas as pd
import plotly.express as px

# Set judul dashboard
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Fungsi untuk memuat dataset
@st.cache_data
def load_data():
    customers = pd.read_csv("customers_dataset.csv")
    orders = pd.read_csv("orders_dataset.csv")
    order_items = pd.read_csv("order_items_dataset.csv")
    products = pd.read_csv("products_dataset.csv")
    product_category = pd.read_csv("product_category_name_translation.csv")

    # Gabungkan product_category dengan products
    products = products.merge(product_category, on="product_category_name", how="left")
    
    return customers, orders, order_items, products

# Load data
customers, orders, order_items, products = load_data()

# Ubah format tanggal pada orders
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Tambahkan kolom bulan untuk analisis tren penjualan (Ubah ke string agar kompatibel dengan JSON)
orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)

# --- SIDEBAR ---
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(orders['order_purchase_timestamp'].dt.year.unique(), reverse=True))

# Filter data berdasarkan tahun yang dipilih
filtered_orders = orders[orders['order_purchase_timestamp'].dt.year == selected_year]

# --- PERTANYAAN 1: POLA PEMBELIAN PELANGGAN ---
st.subheader("📈 Pola Pembelian Pelanggan")
monthly_orders = filtered_orders.groupby('order_month').size().reset_index(name="Jumlah Pesanan")

fig1 = px.line(monthly_orders, x="order_month", y="Jumlah Pesanan", markers=True, title="Tren Jumlah Pesanan per Bulan")
st.plotly_chart(fig1, use_container_width=True)

# --- PERTANYAAN 2: PRODUK ATAU KATEGORI PALING LARIS ---
st.subheader("🛒 Kategori Produk Terlaris")
merged_data = order_items.merge(products, on="product_id", how="left")

# Hitung jumlah produk terjual per kategori
top_categories = merged_data['product_category_name_english'].value_counts().head(10)

fig2 = px.bar(
    x=top_categories.values,
    y=top_categories.index,
    orientation='h',
    title="Top 10 Kategori Produk Terlaris",
    labels={'x': 'Jumlah Produk Terjual', 'y': 'Kategori Produk'},
    color=top_categories.values,
    color_continuous_scale="viridis"
)
st.plotly_chart(fig2, use_container_width=True)

# --- INSIGHT ---
st.subheader("📊 Insight")
st.markdown("""
- **Pola Pembelian Pelanggan**: Jumlah pesanan per bulan menunjukkan adanya lonjakan di bulan-bulan tertentu, kemungkinan terkait dengan promo atau musim liburan.
- **Kategori Produk Terlaris**: Kategori "bed_bath_table" dan "health_beauty" adalah yang paling banyak terjual, menunjukkan permintaan tinggi pada barang rumah tangga dan perawatan diri.
""")
