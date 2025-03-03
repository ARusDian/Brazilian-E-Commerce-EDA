import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from babel.numbers import format_currency
import matplotlib.dates as mdates

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

all_df = pd.read_csv("data/olist_all_data.csv")
for col in datetime:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Brazil E-Commerce Data Analysis")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )


filtered_date_df = all_df[
    (all_df["order_approved_at"] >= str(start_date))
    & (all_df["order_approved_at"] <= str(end_date))
]

preparator = DataPreparator(filtered_date_df)

df_delivered, df_non_delivered, correlation_delivered = (
    preparator.create_orders_delivery_delays_df()
)
st.header(
    "Analisis Delivery Delay dan Review Score pada Order Delivered dan Non-Delivered"
)
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
sns.scatterplot(
    data=df_delivered, x="delivery_delay (days)", y="review_score", alpha=0.5, ax=ax
)
sns.regplot(
    data=df_delivered,
    x="delivery_delay (days)",
    y="review_score",
    scatter=False,
    color="red",
    ax=ax,
)
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
st.subheader(
    "Distribusi Review Score untuk Order Non-Delivered Berdasarkan Status Order"
)
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df_non_delivered, x="order_status", y="review_score", ax=ax)
ax.set_title("Distribusi Review Score untuk Order Non-Delivered")
ax.set_xlabel("Order Status")
ax.set_ylabel("Review Score")
st.pyplot(fig)

agg_payment_trend = preparator.create_payment_method_trend_df()

st.header("Tren Penggunaan Metode Pembayaran")
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
ax.set_title("Tren Penggunaan Metode Pembayaran")
ax.legend()
fig.autofmt_xdate()
st.pyplot(fig)

(
    top_category_total_sales,
    sales_category_trend_top,
    bottom_category_total_sales,
    sales_category_trend_bottom,
) = preparator.create_volume_sales_category_df()

st.header("Analisis Volume Penjualan Berdasarkan Kategori Produk")
st.subheader("Top 5 Kategori Produk dengan Total Penjualan Tertinggi")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=top_category_total_sales,
    x="product_category_name_english",
    y="total_sales",
    hue="product_category_name_english",
    palette="viridis",
    dodge=False,
    ax=ax,
)
ax.set_title(
    "Perbandingan Total Volume Penjualan untuk Top 10 Kategori Produk (1 Tahun Terakhir)"
)
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Total Volume Penjualan")
ax.tick_params(axis='x', rotation=45)
ax.legend([], [], frameon=False)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Bottom 5 Kategori Produk dengan Total Penjualan Terendah")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=bottom_category_total_sales,
    x="product_category_name_english",
    y="total_sales",
    hue="product_category_name_english",
    palette="viridis",
    dodge=False,
    ax=ax,
)
ax.set_title(
    "Perbandingan Total Volume Penjualan untuk Bottom 5 Kategori Produk (1 Tahun Terakhir)"
)
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Total Volume Penjualan")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.legend([], [], frameon=False)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Tren Penjualan Top 5 Kategori Produk")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sales_category_trend_top,
    x="order_month",
    y="sales_count",
    hue="product_category_name_english",
    palette="viridis",
    ax=ax,
)
ax.set_title("Tren Penjualan Top 5 Kategori Produk (1 Tahun Terakhir)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penjualan")
ax.legend(title="Kategori Produk")
fig.autofmt_xdate()
st.pyplot(fig)

st.subheader("Tren Penjualan Bottom 5 Kategori Produk")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sales_category_trend_bottom,
    x="order_month",
    y="sales_count",
    hue="product_category_name_english",
    palette="viridis",
    ax=ax,
)
ax.set_title("Tren Penjualan Bottom 5 Kategori Produk (1 Tahun Terakhir)")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penjualan")
ax.legend(title="Kategori Produk")
fig.autofmt_xdate()
st.pyplot(fig)

st.header("Analisis Korelasi Jumlah Foto Produk dengan Persepsi Pelanggan")


df_photo_review, correlation_photo_qty, avg_photo_review = (
    preparator.create_product_photo_qty_correlation_review_score_df()
)

st.subheader("Distribusi Skor Review berdasarkan Jumlah Foto Produk")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="product_photos_qty", y="review_score", data=df_photo_review, ax=ax)
ax.set_title("Distribusi Skor Review berdasarkan Jumlah Foto Produk")
ax.set_xlabel("Jumlah Foto Produk")
ax.set_ylabel("Skor Review")
st.pyplot(fig)

st.subheader("Hubungan antara Jumlah Foto Produk dan Skor Review dengan Regresi")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="product_photos_qty", y="review_score", data=df_photo_review, alpha=0.6, ax=ax)
sns.regplot(data=df_photo_review, x="product_photos_qty", y="review_score", scatter=False, color="red", ax=ax)
ax.text(
    x=df_photo_review["product_photos_qty"].max() * 0.7,
    y=df_photo_review["review_score"].min() + 0.5,
    s=f"Korelasi: {correlation_photo_qty:.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Hubungan antara Jumlah Foto Produk dan Skor Review dengan Regresi")
ax.set_xlabel("Jumlah Foto Produk")
ax.set_ylabel("Skor Review")
st.pyplot(fig)

st.subheader("Rata-rata Skor Review berdasarkan Jumlah Foto Produk")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="product_photos_qty",
    y="review_score",
    hue="product_photos_qty",
    data=avg_photo_review,
    palette="viridis",
    dodge=False,
    ax=ax,
)
ax.legend_.remove()
ax.set_title("Rata-rata Skor Review berdasarkan Jumlah Foto Produk")
ax.set_xlabel("Jumlah Foto Produk")
ax.set_ylabel("Rata-rata Skor Review")
st.pyplot(fig)

df_photo_sales, correlation_photo_sales, avg_photo_sales = (
    preparator.create_product_photo_qty_correlation_sales_df()
)

st.subheader("Hubungan Jumlah Foto Produk dengan Total Penjualan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="product_photos_qty", y="total_sales", data=df_photo_sales, ax=ax)
sns.regplot(
    x="product_photos_qty",
    y="total_sales",
    data=df_photo_sales,
    scatter=False,
    color="red",
    ax=ax,
)
ax.text(
    x=df_photo_sales["product_photos_qty"].max() * 0.7,
    y=df_photo_sales["total_sales"].min() + 0.5,
    s=f"Korelasi: {correlation_photo_sales:.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Hubungan Jumlah Foto Produk dengan Total Penjualan")
ax.set_xlabel("Jumlah Foto Produk")
ax.set_ylabel("Total Penjualan")
st.pyplot(fig)

st.subheader("Rata-rata Penjualan berdasarkan Jumlah Foto Produk")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="product_photos_qty",
    y="total_sales",
    hue="product_photos_qty",
    data=avg_photo_sales,
    palette="viridis",
    dodge=False,
    ax=ax,
)
ax.legend_.remove()
ax.set_title("Rata-rata Penjualan berdasarkan Jumlah Foto Produk")
ax.set_xlabel("Jumlah Foto Produk")
ax.set_ylabel("Rata-rata Penjualan")
st.pyplot(fig)

st.header("Pengaruh Dimensi Produk terhadap Biaya dan waktu pengiriman, serta dampaknya terhadap Review Pelanggan")

product_dimension_delivery_review_df, product_dimension_delivery_review_corr = (
    preparator.create_product_dimension_correlation_freight_value_delivery_delay_review_score_df()
)

st.subheader("Product Volume vs Freight Value")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=product_dimension_delivery_review_df,
    x="product_volume_cm3",
    y="freight_value",
    scatter_kws={"s": 30},
    line_kws={"color": "red"},
    ax=ax,
)
ax.text(
    x=product_dimension_delivery_review_df["product_volume_cm3"].max() * 0.7,
    y=product_dimension_delivery_review_df["freight_value"].min() + 0.5,
    s=f"Corr: {product_dimension_delivery_review_df['product_volume_cm3'].corr(product_dimension_delivery_review_df['freight_value']):.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Product Volume vs Freight Value")
ax.set_xlabel("Product Volume (cm³)")
ax.set_ylabel("Freight Value")
st.pyplot(fig)

st.subheader("Product Volume vs Shipping Time (Days)")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=product_dimension_delivery_review_df,
    x="product_volume_cm3",
    y="shipping_time_days",
    scatter_kws={"s": 30},
    line_kws={"color": "red"},
    ax=ax,
)
ax.text(
    x=product_dimension_delivery_review_df["product_volume_cm3"].max() * 0.7,
    y=product_dimension_delivery_review_df["shipping_time_days"].min() + 0.5,
    s=f"Corr: {product_dimension_delivery_review_df['product_volume_cm3'].corr(product_dimension_delivery_review_df['shipping_time_days']):.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Product Volume vs Shipping Time (Days)")
ax.set_xlabel("Product Volume (cm³)")
ax.set_ylabel("Shipping Time (days)")
st.pyplot(fig)

st.subheader("Product Weight vs Freight Value")
fig, ax = plt.subplots(figsize=(10, 6))
sns.regplot(
    data=product_dimension_delivery_review_df,
    x="product_weight_g",
    y="freight_value",
    scatter_kws={"s": 30},
    line_kws={"color": "red"},
    ax=ax,
)
ax.text(
    x=product_dimension_delivery_review_df["product_weight_g"].max() * 0.7,
    y=product_dimension_delivery_review_df["freight_value"].min() + 0.5,
    s=f"Corr: {product_dimension_delivery_review_df['product_weight_g'].corr(product_dimension_delivery_review_df['freight_value']):.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)
ax.set_title("Product Weight vs Freight Value")
ax.set_xlabel("Product Weight (g)")
ax.set_ylabel("Freight Value")
st.pyplot(fig)

st.subheader("Product Volume vs Review Score")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=product_dimension_delivery_review_df, x="review_score", y="product_volume_cm3", ax=ax)
ax.set_title("Product Volume vs Review Score")
ax.set_xlabel("Review Score")
ax.set_ylabel("Product Volume (cm³)")
st.pyplot(fig)

st.subheader("Product Weight vs Review Score")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=product_dimension_delivery_review_df, x="review_score", y="product_weight_g", ax=ax)
ax.set_title("Product Weight vs Review Score")
ax.set_xlabel("Review Score")
ax.set_ylabel("Product Weight (g)")
st.pyplot(fig)

st.subheader("Matriks Korelasi antara Dimensi Produk, Pengiriman, dan Review")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    product_dimension_delivery_review_corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax
)
ax.set_title("Matriks Korelasi antara Dimensi Produk, Pengiriman, dan Review")
st.pyplot(fig)

top_categories, bottom_categories = preparator.create_category_sales_df()

st.header("Analisis Penjualan Terlaris dan Terendah Berdasarkan Kategori Produk")
plt.figure(figsize=(16, 6))
st.subheader("Top 10 Kategori Produk Berdasarkan Penjualan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=top_categories,
    x="total_sales",
    y="product_category_name_english",
    hue="product_category_name_english",
    dodge=False,
    palette="viridis",
    ax=ax,
)
ax.set_title("Top 10 Kategori Produk Berdasarkan Penjualan")
ax.set_xlabel("Total Penjualan")
ax.set_ylabel("Kategori Produk")
ax.legend([], [], frameon=False)
st.pyplot(fig)

# Chart untuk Bottom 10 Kategori Produk
st.subheader("Bottom 10 Kategori Produk Berdasarkan Penjualan")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=bottom_categories.sort_values("total_sales", ascending=True),
    x="total_sales",
    y="product_category_name_english",
    hue="product_category_name_english",
    dodge=False,
    palette="viridis",
    ax=ax,
)
ax.set_title("Bottom 10 Kategori Produk Berdasarkan Penjualan")
ax.set_xlabel("Total Penjualan")
ax.set_ylabel("Kategori Produk")
ax.legend([], [], frameon=False)
st.pyplot(fig)
