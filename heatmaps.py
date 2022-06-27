import requests
import pandas as pd
import time
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
place1 = st.empty()
place2 = st.empty()
df = pd.DataFrame()
place3 = st.empty()
place4 = st.empty()
df1 = pd.DataFrame()
for i in range(20):
    df = pd.concat([df, pd.json_normalize(requests.get("https://api.cryptowat.ch/markets/kraken/btcusd/orderbook").json()["result"]).assign(timestamp=pd.to_datetime("now", utc=True))])
    d = df.loc[:, ["timestamp", "asks"]].explode("asks").assign(
    price=lambda d: d["asks"].apply(lambda a: a[0]),
    size=lambda d: d["asks"].apply(lambda a: a[1]),
    
    
    
    )


    df1 = pd.concat([df1, pd.json_normalize(requests.get("https://api.cryptowat.ch/markets/kraken/btcusd/orderbook").json()["result"]).assign(timestamp=pd.to_datetime("now", utc=True))])
    f = df1.loc[:, ["timestamp", "bids"]].explode("bids").assign(
    price=lambda f: f["bids"].apply(lambda a: a[0]),
    size=lambda f: f["bids"].apply(lambda a: a[1]),
    
    
    
    )

    with place3.container():
        st.plotly_chart(px.scatter(f, x="timestamp", y="price", size="size"))
    with place1.container():
        st.plotly_chart(px.scatter(d, x="timestamp", y="price", size="size"))
    with place2.container():
        st.plotly_chart(go.Figure(go.Heatmap(x=d["timestamp"], y=d["price"], z=d["size"] , colorscale="plasma")))
    with place4.container():
        st.plotly_chart(go.Figure(go.Heatmap(x=f["timestamp"], y=f["price"], z=f["size"] , colorscale="solar")))        # st.write(df1)
    time.sleep(1)

# for i in range(20):

#     time.sleep(1)

