import pandas as pd
import statsmodels.api as sm
from sklearn.cluster import KMeans

def regression_analysis(df: pd.DataFrame):
    """OLS regression of returns vs volatility."""
    df = df.dropna()
    X = df[["Volatility20"]]
    X = sm.add_constant(X)
    y = df["Returns"]
    model = sm.OLS(y, X).fit()
    return model.summary()

def volatility_clusters(df: pd.DataFrame, n_clusters=3):
    """Cluster days by volatility and returns."""
    X = df[["Volatility20", "Returns"]].dropna()
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X)
    df.loc[X.index, "VolCluster"] = kmeans.labels_
    return df
