import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from babel.numbers import format_currency

from dashboard_util import DataPreparator

sns.set(style="dark")

datetime = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "order_purchase_timestamp",
    "shipping_limit_date",
]

# Dataset
all_df = pd.read_csv("data/olist_all_data.csv")

preparator = DataPreparator(all_df)

for col in datetime:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Brazil E-Commerce Data Analysis")

    # Logo Image
    # st.image("./date_img.jpg")

    # Date Range
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

df_delivered, df_non_delivered, correlation_delivered = (
    preparator.create_orders_delivery_delays_df()
)
st.header("Analisis Delivery Delay dan Review Score pada Order Delivered dan Non-Delivered")
# Box Plot Distribusi Review Score untuk Order Delivered
st.subheader("Distribusi Review Score untuk Order Delivered")
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df_delivered, y="delivery_delay (days)", ax=ax)
ax.set_title("Distribusi Review Score untuk Order Delivered")
ax.set_ylabel("Review Score")
st.pyplot(fig)

# Scatter Plot dengan Regresi untuk Order Delivered
st.subheader("Hubungan antara Delivery Delay dan Review Score (Order Delivered)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_delivered, x="delivery_delay (days)", y="review_score", alpha=0.5, ax=ax)
sns.regplot(data=df_delivered, x="delivery_delay (days)", y="review_score", scatter=False, color="red", ax=ax)
ax.text(
    x=df_delivered["delivery_delay (days)"].max() * 0.7,
    y=df_delivered["review_score"].min() + 0.5,
    s=f"Corr: {correlation_delivered:.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Hubungan antara Delivery Delay dan Review Score (Order Delivered)")
ax.set_xlabel("Delivery Delay (hari)")
ax.set_ylabel("Review Score")
st.pyplot(fig)

# Box Plot Distribusi Review Score untuk Order Non-Delivered Berdasarkan Status Order
st.subheader("Distribusi Review Score untuk Order Non-Delivered Berdasarkan Status Order")
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df_non_delivered, x="order_status", y="review_score", ax=ax)
ax.set_title("Distribusi Review Score untuk Order Non-Delivered")
ax.set_xlabel("Order Status")
ax.set_ylabel("Review Score")
st.pyplot(fig)

agg_payment_trend = preparator.create_payment_method_trend_df()

st.header("Tren Penggunaan Metode Pembayaran (2 Tahun Terakhir Berdasarkan Tanggal Terbaru)")
fig, ax = plt.subplots(figsize=(12, 6))
for payment in agg_payment_trend["payment_type"].unique():
    subset = agg_payment_trend[agg_payment_trend["payment_type"] == payment]
    ax.plot(
        subset["month"],
        subset["transaction_count"],
        marker="o",
        label=payment,
    )
ax.grid(True)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Transaksi")
ax.set_title("Tren Penggunaan Metode Pembayaran (2 Tahun Terakhir Berdasarkan Tanggal Terbaru)")
ax.legend()
fig.autofmt_xdate()
st.pyplot(fig)
