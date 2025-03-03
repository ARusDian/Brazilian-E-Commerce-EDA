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
all_df = pd.read_csv(./"data/olist_all_data.csv")

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

plt.figure(figsize=(8, 6))
sns.boxplot(data=df_delivered, y="delivery_delay (days)")
plt.title("Distribusi Review Score untuk Order Delivered")
plt.ylabel("Review Score")
plt.show()

# Scatter Plot dengan Regresi untuk Order Delivered
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_delivered, x="delivery_delay (days)", y="review_score", alpha=0.5
)

# Plot regresi
sns.regplot(
    data=df_delivered,
    x="delivery_delay (days)",
    y="review_score",
    scatter=False,
    color="red",
)

plt.text(
    x=df_delivered["delivery_delay (days)"].max() * 0.7,
    y=df_delivered["review_score"].min() + 0.5,
    s=f"Corr: {correlation_delivered:.4f}",
    fontsize=12,
    color="red",
    bbox=dict(facecolor="white", alpha=0.7, edgecolor="red"),
)

plt.title("Hubungan antara Delivery Delay dan Review Score (Order Delivered)")
plt.xlabel("Delivery Delay (hari)")
plt.ylabel("Review Score")
plt.show()


# Box Plot Distribusi Review Score untuk Order Non-Delivered Berdasarkan Status Order
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_non_delivered, x="order_status", y="review_score")
plt.title("Distribusi Review Score untuk Order Non-Delivered")
plt.xlabel("Order Status")
plt.ylabel("Review Score")
plt.show()
