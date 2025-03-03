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

for col in datetime:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("M. Nandaarjuna F.")

    # Logo Image
    # st.image("./date_img.jpg")

    # Date Range
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )
