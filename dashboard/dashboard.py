import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    customers = pd.read_csv("data/customers_dataset.csv")
    orders = pd.read_csv("data/orders_dataset.csv")
    order_items = pd.read_csv("data/order_items_dataset.csv")
    products = pd.read_csv("data/products_dataset.csv")
    product_category = pd.read_csv("data/product_category_name_translation.csv")

    products = products.merge(product_category, on="product_category_name", how="left")
    
    return customers, orders, order_items, products

customers, orders, order_items, products = load_data()

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)

st.sidebar.header("Filter Data")
year_options = ["All Years"] + sorted(orders['order_purchase_timestamp'].dt.year.unique(), reverse=True)
selected_year = st.sidebar.selectbox("Pilih Tahun", year_options)

if selected_year == "All Years":
    filtered_orders = orders
else:
    filtered_orders = orders[orders['order_purchase_timestamp'].dt.year == selected_year]

st.subheader("📈 Pola Pembelian Pelanggan")
monthly_orders = filtered_orders.groupby('order_month').size().reset_index(name="Jumlah Pesanan")

fig1 = px.line(
    monthly_orders, 
    x="order_month", 
    y="Jumlah Pesanan", 
    markers=True, 
    title="Tren Jumlah Pesanan per Bulan",
    labels={"order_month": "Bulan", "Jumlah Pesanan": "Jumlah Pesanan"}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🛒 Kategori Produk Terlaris")
merged_data = order_items.merge(products, on="product_id", how="left")

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

st.subheader("📊 Insight")
st.markdown("""
- **Pola Pembelian Pelanggan**: Jumlah pesanan per bulan menunjukkan adanya lonjakan di bulan-bulan tertentu, kemungkinan terkait dengan promo atau musim liburan.
- **Kategori Produk Terlaris**: Kategori "bed_bath_table" dan "health_beauty" adalah yang paling banyak terjual, menunjukkan permintaan tinggi pada barang rumah tangga dan perawatan diri.
""")
