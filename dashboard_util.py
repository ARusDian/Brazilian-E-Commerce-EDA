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
