import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisis E-commerce", layout="wide")

st.title("📊 Dashboard Analisis Data E-commerce")
st.markdown("Dashboard ini menampilkan statistik pendapatan kategori produk dan performa pengiriman untuk menjawab pertanyaan bisnis utama perusahaan.")
st.markdown("---")


@st.cache_data
def load_data():
    df_pendapatan = pd.read_csv("./dashboard/pendapatan_kategori.csv")
    df_pengiriman = pd.read_csv("./dashboard/pengiriman_terlambat.csv")
    
    if 'True' in df_pengiriman.columns and 'False' in df_pengiriman.columns:
        df_pengiriman['Total_Pengiriman'] = df_pengiriman['True'] + df_pengiriman['False']
        df_pengiriman = df_pengiriman.rename(columns={'True': 'Jumlah_Terlambat'})
        df_pengiriman['Persentase_Terlambat_State'] = (df_pengiriman['Jumlah_Terlambat'] / df_pengiriman['Total_Pengiriman']) * 100
        
    return df_pendapatan, df_pengiriman

df_pendapatan, df_pengiriman = load_data()

total_penjualan = df_pendapatan['total_pendapatan'].sum()
st.subheader("1. Total Pendapatan Kategori")
st.metric(label="Total Pendapatan (BRL)", value=f"R$ {total_penjualan:,.2f}")
st.write("")

top_5_kategori = df_pendapatan.head(5)
fig_kategori = px.bar(
    top_5_kategori, 
    x='product_category_name_english', 
    y='total_pendapatan', 
    title='Top 5 Kategori Berdasarkan Total Pendapatan',
    labels={'product_category_name_english': 'Kategori Produk', 'total_pendapatan': 'Total Pendapatan (R$)'},
    text_auto='.2s',
    color='total_pendapatan',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_kategori, use_container_width=True)

st.markdown("---")
st.subheader("2. Analisis Performa Pengiriman per Negara Bagian")

col1, col2, col3 = st.columns(3)

with col1:
    fig_total_pengiriman = px.bar(
        df_pengiriman.sort_values('Total_Pengiriman', ascending=False).head(10),
        x='customer_state', 
        y='Total_Pengiriman',
        title='Total Pengiriman (Volume)',
        labels={'customer_state': 'State', 'Total_Pengiriman': 'Jumlah Paket'},
        color_discrete_sequence=['#3498DB']
    )
    st.plotly_chart(fig_total_pengiriman, use_container_width=True)


with col2:
    fig_jumlah_terlambat = px.bar(
        df_pengiriman.sort_values('Jumlah_Terlambat', ascending=False).head(10),
        x='customer_state', 
        y='Jumlah_Terlambat',
        title='Jumlah Keterlambatan (Angka Absolut)',
        labels={'customer_state': 'State', 'Jumlah_Terlambat': 'Total Paket Terlambat'},
        color_discrete_sequence=['#F39C12'] 
    )
    st.plotly_chart(fig_jumlah_terlambat, use_container_width=True)


with col3:
    fig_persentase_terlambat = px.bar(
        df_pengiriman.sort_values('Persentase_Terlambat_State', ascending=False).head(10), 
        x='customer_state', 
        y='Persentase_Terlambat_State',
        title='Persentase Keterlambatan (%)',
        labels={'customer_state': 'State', 'Persentase_Terlambat_State': 'Persentase Terlambat (%)'},
        color_discrete_sequence=['#E74C3C'] 
    )
    st.plotly_chart(fig_persentase_terlambat, use_container_width=True)

st.markdown("---")