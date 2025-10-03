import streamlit as st
from api_client import fetch_market_data
from data_processing import add_features
from analysis import regression_analysis, volatility_clusters
import matplotlib.pyplot as plt

st.title("📊 Market Analysis API Dashboard")

ticker = st.text_input("Enter Ticker Symbol", "AAPL")
df = fetch_market_data(ticker)
df = add_features(df)

st.line_chart(df[["Close", "MA20", "MA50"]])

# Advanced analysis
st.subheader("Regression Analysis")
st.text(regression_analysis(df))

df = volatility_clusters(df)
st.subheader("Volatility Clusters")
st.write(df[["Date", "Returns", "Volatility20", "VolCluster"]].tail())
