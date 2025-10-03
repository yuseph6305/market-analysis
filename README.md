# market-analysis
# Market Data Pricing Tool

## Overview
The **Market Data Pricing Tool** is a **Python + Streamlit application** that automates **bid/ask spread analysis** on historical market datasets. It uses **Pandas** for data processing, **scikit-learn** for clustering and regression, and provides **interactive visualizations** to deliver faster and more actionable pricing insights.  

## Features
- Automated **data pipeline** for processing large historical datasets  
- **Bid/ask spread analysis** with statistical and machine learning methods  
- **Interactive dashboard** powered by Streamlit  
- **Data visualization** for clearer pricing insights  
- Export results to **Excel/CSV** for further reporting  

## Tech Stack
- **Python 3.12+**  
- **Pandas** – data cleaning & transformation  
- **scikit-learn** – clustering & regression models  
- **Streamlit** – interactive web app interface  
- **Excel/CSV** – input & output data  

## 📂 Project Structure
│── analysis.py # Bid/ask spread analysis functions
│── data_processing.py # Data pipeline and preprocessing
│── streamlit_app.py # Streamlit dashboard
│── api_client.py # API/data loading logic (if used)
│── requirements.txt # Dependencies
│── market_quotes_large.csv # Sample dataset
