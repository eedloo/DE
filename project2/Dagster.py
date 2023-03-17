from dagster import asset
import pandas as pd
import numpy as np
from pandas import DataFrame, read_excel, read_csv, read_html
import Pipeline

@asset
def car_stocks() -> DataFrame:
    cs_df = pd.read_excel('./data/car_stocks.xlsx')
    dic = Pipeline.extract(cs_df)
    pchfy = Pipeline.mchange(dic)
    data = Pipeline.agg(dic, pchfy)
    stock_df = Pipeline.make_df(data)
    return stock_df

@asset
def car_prices() -> DataFrame:
    cpp_df = Pipeline.cpp()
    return cpp_df

@asset
def car_color() -> DataFrame:
    color_df = Pipeline.color()
    return color_df

@asset
def customer_CI() -> DataFrame:
    cci_df = Pipeline.cci()
    return cci_df

@asset
def analytic_car_data(car_prices: DataFrame, car_stocks: DataFrame, car_color: DataFrame, customer_CI: DataFrame) -> DataFrame:
    merged_df = Pipeline.merge(car_prices, car_stocks, car_color, customer_CI)
    return merged_df
