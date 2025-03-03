import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import os
from colorama import Fore, Style
import folium
from folium.plugins import HeatMap, MarkerCluster
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


class DataPreparator:
    def __init__(self, df):
        self.df = df

    def create_orders_delivery_delays_df(self):
        df_orders = self.df.copy()
        # Menghitung selisih antara tanggal estimasi pengiriman dan tanggal aktual dalam detik
        df_orders["delivery_delay (days)"] = (
            df_orders["order_estimated_delivery_date"]
            - df_orders["order_delivered_customer_date"]
        ).dt.days

        df_delivered = df_orders[df_orders["order_status"] == "delivered"].copy()
        df_non_delivered = df_orders[df_orders["order_status"] != "delivered"].copy()

        correlation_delivered = df_delivered["delivery_delay (days)"].corr(
            df_delivered["review_score"]
        )

        return df_delivered, df_non_delivered, correlation_delivered

    def create_payment_method_trend_df(self):
        payment_methods = self.df["payment_type"].unique()

        order_wpayments = self.df.copy()

        latest_date = order_wpayments["order_purchase_timestamp"].max()

        start_date = latest_date - pd.DateOffset(years=2)

        filtered_data = order_wpayments[
            order_wpayments["order_purchase_timestamp"] >= start_date
        ].copy()

        filtered_data["month"] = (
            filtered_data["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
        )

        agg_data = (
            filtered_data.groupby(["month", "payment_type"])
            .size()
            .reset_index(name="transaction_count")
        )

        agg_data = agg_data.sort_values(by="month") 

        return agg_data
