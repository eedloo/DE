from dagster import asset
import pandas as pd
from pandas import DataFrame, read_excel, read_csv

@asset
def car_stocks() -> DataFrame:
    df = read_excel('./data/car_stocks.xlsx')
    return df

@asset
def car_prices() -> DataFrame:
    df = read_csv('./data/car_price_prediction.csv')
    return df

@asset
def car_stocks_hi_lo(car_stocks: DataFrame) -> DataFrame:
    df = car_stocks.pivot(index='Manufacturer', columns='Date', values='Closing Price')
    return df

@asset
def analytic_car_data(car_stocks_hi_lo: DataFrame, car_prices: DataFrame) -> DataFrame:
    df = car_prices.merge(car_stocks_hi_lo, how='left', on='Manufacturer')
    return df