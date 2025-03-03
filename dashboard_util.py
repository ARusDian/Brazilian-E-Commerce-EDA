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
            filtered_data["order_purchase_timestamp"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        agg_data = (
            filtered_data.groupby(["month", "payment_type"])
            .size()
            .reset_index(name="transaction_count")
        )

        agg_data = agg_data.sort_values(by="month")

        return agg_data

    def create_volume_sales_category_df(self):
        df = self.df.copy()

        latest_date = df["order_purchase_timestamp"].max()

        start_date = latest_date - pd.DateOffset(years=1)

        order_product = df[df["order_purchase_timestamp"] >= start_date]

        order_product.loc[:, "order_month"] = (
            order_product["order_purchase_timestamp"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        sales_trend = (
            order_product.groupby(["order_month", "product_category_name_english"])
            .size()
            .reset_index(name="sales_count")
        )

        total_sales = (
            order_product.groupby("product_category_name_english")
            .size()
            .reset_index(name="total_sales")
        ).sort_values("total_sales", ascending=False)

        top_categories = (
            total_sales.sort_values("total_sales", ascending=False)
            .head(10)["product_category_name_english"]
            .tolist()
        )

        top_total_sales = total_sales[
            total_sales["product_category_name_english"].isin(top_categories)
        ]

        sales_trend_top = sales_trend[
            sales_trend["product_category_name_english"].isin(top_categories)
        ]

        bottom_categories = total_sales.tail(10)[
            "product_category_name_english"
        ].tolist()

        bottom_total_sales = total_sales[
            total_sales["product_category_name_english"].isin(bottom_categories)
        ].sort_values("total_sales", ascending=True)

        sales_trend_bottom = sales_trend[
            sales_trend["product_category_name_english"].isin(bottom_categories)
        ]

        return top_total_sales, sales_trend_top, bottom_total_sales, sales_trend_bottom

    def create_product_photo_qty_correlation_review_score_df(self):
        df = self.df.copy()

        product_photo_qty = df["product_photos_qty"].unique()

        correlation_photo_qty = df["product_photos_qty"].corr(df["review_score"])

        avg_review = (
            df.groupby("product_photos_qty")["review_score"].mean().reset_index()
        )

        return df, correlation_photo_qty, avg_review

    def create_product_photo_qty_correlation_sales_df(self):
        df = self.df.copy()

        product_wsales = df.merge(
            df.groupby("product_id")["order_item_id"]
            .count()
            .reset_index(name="total_sales"),
            on="product_id",
            how="inner",
        )

        correlation_photo_qty = df["product_photos_qty"].corr(
            product_wsales["total_sales"]
        )

        avg_sales = (
            df.groupby("product_photos_qty")["order_item_id"]
            .count()
            .reset_index(name="avg_sales")
        )

        return product_wsales, correlation_photo_qty, avg_sales
