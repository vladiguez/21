import streamlit as st
import requests
import json
import pandas as pd
import math
import time
from itertools import accumulate
# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import chain

import plotly.express as px
from datetime import datetime, timedelta
# ts = int('1645598410')

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
import json
import requests
import pandas as pd
import random
st.set_page_config(layout="wide")

import asyncio
from asyncio import futures
# from glob import glob
# from numpy import full_like
# from rx import empty
import websockets
import json
import streamlit as st
import pandas as pd
# import time
# import plotly.express as px
# from itertools import accumulate
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# st.set_page_config(layout="wide")
# placeholder1 = st.empty()
merge_v2_USD = pd.DataFrame()
# df = pd.DataFrame(columns = ['id', 'price', 'size', 'side', 'liquidation', 'time'])
placeholder = st.empty()
placeholder2 = st.empty()
# # for seconds in range(200):
# # while True: 
# dict_dumps = {
#   "op": "subscribe",
#   "channel": "trades",
#   "market": "BTC-PERP"
# }
d ={'i':[],'asset':[],'PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY':[],'PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE_APY':[], 'PREMIUM_LONG_SPOT_SHORT_PERP_APY':[], 'PREMIUM_SHORT_SPOT_LONG_PERP_APY':[],'PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY':[],'PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY':[]}
cash_n_carrydf = pd.DataFrame(d)
# name = st.text_input("market name", "BTC-PERP")
# dict_dumps["market"] = name
# dumps =  '''{"op": "subscribe", "channel": "trades", "market": ''' 
# rest = f'''"{name}"'''
# last = "}"
# full_dump = dumps + rest + last
# full_dump.astype(dict)
# st.write(dict_dumps)

async def consumer() -> None:
    async with websockets.connect("wss://ftx.com/ws/", ping_interval=20, ping_timeout=2000) as websocket:
        await websocket.send(json.dumps({"op": "subscribe", "channel": "markets"}))
        async for message in websocket:
            message = json.loads(message)
            global merge_v2_USD
            with placeholder.container():
                if message["type"] == "partial":
                    data_init = message['data']
                    data = data_init['data']
                    namez = pd.DataFrame.from_dict(data)
                    names = namez.iloc[0]
                    names = pd.DataFrame(names)    
                    types = namez.iloc[5].dropna()
                    types = pd.DataFrame(types)
                    merged = names.merge(types, left_index=True, right_index=True)
                    spot = merged.loc[merged["type"] == "spot"]
                    merged['expiry'] = merged['name'].str[-4:]
                    perpsz = merged.loc[merged["expiry"] == "PERP"]
                    perpsz['name_shorten_perps'] = perpsz["name"].str[:-5]
                    perpsz = perpsz.drop(columns=['type'])
                    dated = merged.loc[merged["type"] != "spot"]
                    dated = dated.loc[dated["expiry"] != "PERP"]
                    dated['name_shorten_dated'] = dated["name"].str[:-5]
                    dated = dated.drop(columns=['type'])
                    base = namez.iloc[6]
                    quote = namez.iloc[7]
                    base = pd.DataFrame(base)
                    quote = pd.DataFrame(quote)
                    base = base.dropna()
                    quote = quote.dropna()
                    base_quote = base.merge(quote, left_index=True, right_index=True)
                    base_quote_spot = base_quote.merge(spot, left_index=True, right_index=True)
                    merge_v1 = base_quote_spot.merge(dated, left_on="baseCurrency",right_on="name_shorten_dated")
                    merge_v2 = merge_v1.merge(perpsz, left_on="baseCurrency",right_on="name_shorten_perps")
                    merge_v2_USD = merge_v2.loc[merge_v2["quoteCurrency"] == "USD"]

            # st.write("triangular", merge_v2_USD)
                    break
                    # break
asyncio.run(consumer())
st.write(merge_v2_USD)
merge_v2_USD = pd.DataFrame(merge_v2_USD)
new = merge_v2_USD[['name_x','name_y','name', 'baseCurrency']]
# new = new.to_dict(orient='records')
st.write(new)
placeholder1 = st.empty()
i = 0

for index, row in new.iterrows():

    with placeholder1.container():
        # global cash_n_carrydf

# st.write(row['name_x'], row['name_y'], row['name'])
        spot = row['name_x']
        dated = row['name_y']
        perp = row['name']
        lending = row['baseCurrency']
        st.write(spot, dated, perp, lending)

# st.text('comments 1')
# st.markdown('_Markdown_') # see *
# st.latex(r''' e^{i\pi} + 1 = 0 ''')
# st.write('Most objects') # df, err, func, keras!
# st.write(['st', 'is <', 3]) # see *
# st.title('My title')
# st.header('My header')
# st.subheader('My sub')
# st.code('for i in range(8): foo()')



# premiums = requests.get('https://ftxpremiums.com/assets/data/premiums.json')
# premiums = json.loads(premiums.text)
# premiums = pd.DataFrame(premiums)
# print(premiums)
# st.write("cash and carry premiums")
# st.write(premiums)
# lending = requests.get('https://ftxpremiums.com/assets/data/lending.json')
# lending = json.loads(lending.text)
# lending = pd.DataFrame(lending)
# # print(lending)    
# # st.write("lending rates")

# # st.write(lending)
# funding = requests.get('https://ftxpremiums.com/assets/data/funding.json')
# funding = json.loads(funding.text)
# funding = pd.DataFrame(funding)
# # print(funding)
# st.write("funding rates")

# st.write(funding)
# premiums_names = premiums['name']
# premiums_names.sort_values(ascending=True)
# 

# lending_names = lending['name']
# # st.write(lending_names)

# perp_names = funding['name']
# # st.write(perp_names)

# names_premeiums = 'BTC/USD'
# @st.cache
# st.title("HERE CREAMY D CLIUVK HERE")
# st.write(names_premeiums)
# funding = pd.read_csv('funding.csv')
# lending = pd.read_csv('lending.csv')

# premiums = pd.read_csv('premiums.csv')
    names_premeiums = dated
    # names_premeiums = st.selectbox("premiums", premiums, index = here)
    # st.write(names_premeiums)
    names_lending = spot 
    # = st.selectbox("lending", lending
    # ,

    #  index = 3)
    # st.write(names_lending)
    name_perp = perp
    # = st.selectbox("perp", funding

    # , index = random.randint(0, 10)
    # )

    # st.write(names_premeiums)
    # st.title('dated futures')
    df0 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/candles?resolution=14400").json()
    # st.write(df)
    df0 = pd.DataFrame(df0['result'])

    # st.write(df)
    # Create figure with secondary y-axis
    fig0 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig0.add_trace(go.Candlestick(x=df0['startTime'],open=df0['open'], high=df0['high'],low=df0['low'], close=df0['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig0.add_trace(go.Bar(x=df0['startTime'], y=df0['volume'],
                showlegend=False), row=2, col=1)

    fig0.update(layout_xaxis_rangeslider_visible=False)
    # st.plotly_chart(fig0, use_container_width=True)


    df1 = requests.get(f"https://ftx.com/api/markets/{names_premeiums}/orderbook?depth=100").json()
    df1 = pd.DataFrame(df1)
    # names_premeiums = BTC-0930
    expiry = names_premeiums.split('-')[1]
    expiry = pd.to_datetime(expiry, format='%m%d')
    # """ year is the same as this year"""
    expiry = expiry.replace(year=datetime.now().year)
    # st.write("expiry date", expiry)

    # expiry = datetime.datetime.strftime(expiry,'%m%d')
    days_until_expiry = expiry - datetime.now()
    # """between now and expiry"""

    # st.write(int(datetime.now().('%m%d'strftime)))
    # days_until_expiry = ((expiry).strftime('%m%d')) - (datetime.now().strftime('%m%d'))
    # st.write("now",datetime.now())
    # st.write("days until expiry: ", days_until_expiry)
    # st.write("add the amount of funding events until expiry ")


    pct_expiry_dated = days_until_expiry.days / 365 * 100
    # st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")






    df1 = df1['result']
    asks = df1['asks']
    bids = df1['bids']
    asks = pd.DataFrame(asks)
    bids = pd.DataFrame(bids)
    asks = asks.rename(columns={0: "price", 1: "size"})
    bids = bids.rename(columns={0: "price", 1: "size"})

    asks['accumulated_size']  = (list(accumulate(asks['size'])))
    asks['accumulated_price']  = (asks['price']) * asks['size']
    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
    asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


    bids['accumulated_size']  = (list(accumulate(bids['size'])))
    bids['accumulated_price']  = (bids['price']) * bids['size']
    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
    bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']




    column = bids["price"]
    max_value_dated_futures = column.max()
    # st.write("best ask dated futures", max_value_dated_futures)


    column = asks["price"]
    min_value_dated_futures = column.min()
    # st.write("best bid dated futures", min_value_dated_futures)

    spred_dated = min_value_dated_futures - max_value_dated_futures
    # st.write("spread dated futures", spred_dated)



    spred_dated_BPS = spred_dated/min_value_dated_futures*1000
    # st.write("spread dated futures", spred_dated_BPS, "bps")
    # asks['price'] = asks[0]
    # asks['size'] = asks[1]
    # for i in range(1, 2):
    #     cols = st.columns(2)
    #     cols[0].subheader("bids")

    #     cols[0].write(bids)
    #     cols[1].subheader("asks")

    #     cols[1].write(asks)
        
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=asks['price'], y=asks['accumulated_size'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['price'], y=bids['accumulated_size'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)



    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=asks['price'], y=asks['size'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Bar(x=bids['price'], y=bids['size'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)








    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="cash_equivelant"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)















    # st.write(names_lending)
    # st.title('spot/usd/lending')

    dft2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/candles?resolution=14400").json()
    # st.write(df)
    dft2 = pd.DataFrame(dft2['result'])

    # st.write(df)
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
            row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=dft2['startTime'],open=dft2['open'], high=dft2['high'],low=dft2['low'], close=dft2['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=dft2['startTime'], y=dft2['volume'],
            showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    # st.plotly_chart(fig, use_container_width=True)


    









    df2 = requests.get(f"https://ftx.com/api/markets/{names_lending}/orderbook?depth=100").json()
    # st.write(df2)
    # df2 = pd.DataFrame(df2)
    df2 = pd.DataFrame(df2)
    df2 = df2['result']
    asks = df2['asks']
    bids = df2['bids']
    asks = pd.DataFrame(asks)
    bids = pd.DataFrame(bids)
    # asks = asks.rename(columns={0: "price", 1: "size"})
    # bids = bids.rename(columns={0: "price", 1: "size"})
    # st.write(bids, asks)
    asks = asks.rename(columns={0: "price", 1: "size"})
    bids = bids.rename(columns={0: "price", 1: "size"})
    asks['accumulated_size']  = (list(accumulate(asks['size'])))
    asks['accumulated_price']  = (asks['price']) * asks['size']
    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated_size']
    asks['cash_equivelant'] = asks['accumulated_size'] * asks['accumulated_avg_price']


    bids['accumulated_size']  = (list(accumulate(bids['size'])))
    bids['accumulated_price']  = (bids['price']) * bids['size']
    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated_size']
    bids['cash_equivelant'] = bids['accumulated_size'] * bids['accumulated_avg_price']
    column = bids["price"]
    max_value_spot = column.max()
    # st.write("now",datetime.now())
    # st.write("best bid", max_value_spot)

    column = asks["price"]
    min_value_spot = column.min()
    # st.write("best ask", min_value_spot)

    spred_spot = min_value_spot - max_value_spot
    # st.write("spot spread", spred_spot)

    spred_bps_spot = spred_spot/min_value_spot*1000
    # st.write("spred_bps", spred_bps_spot , "bps")
    # asks['price'] = asks[0]
    # asks['size'] = asks[1]
    # for i in range(1, 2):
    #     cols = st.columns(2)
    #     cols[0].subheader("bids")
    #     cols[0].write(bids)
    #     cols[1].subheader("asks")

    #     cols[1].write(asks)


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=asks['price'], y=asks['accumulated_size'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['price'], y=bids['accumulated_size'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=asks['price'], y=asks['size'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Bar(x=bids['price'], y=bids['size'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)








    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="cash_equivelant"
    )

    # Set x-axis title

    # latest_rateAPY_spot = 0.0000001
    # latest_rate_bps_hr = 0.00000001
    # st.plotly_chart(fig, use_container_width=True)
    names_lending = lending
    custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={names_lending}&start_time=960368456&end_time=1854597556").json()

    # def test():
    #     global latest_rateAPY_spot
    #     global latest_rate_bps_hr
    #     global names_lending
    # # """if the requesst is not sucessfull print fail"""
    #     custom_lending = requests.get(f"https://ftx.com/api/spot_margin/history?coin={names_lending}&start_time=960368456&end_time=1854597556").json()
    #     # st.write(custom_lending)
    #     # with placeholder2:

    if custom_lending['success'] == True: 
        if custom_lending['result'] != []:
            # with placeholder2():
            custom_lending = pd.DataFrame(custom_lending['result'])
            # st.write(custom_lending)
            custom_lending['rate'] = custom_lending['rate'].astype(float)
            custom_lending['time'] =  pd.to_datetime(custom_lending['time'])
            custom_lending = custom_lending.sort_values(by="time", ascending=True)

            # custom_lending['accumulated']  = (list(accumulate(custom_lending['rate'] * custom_lending['size'])))

            custom_lending['rateAPY'] = custom_lending['rate'] * 24 * 36500
            custom_lending['interest'] = custom_lending['rate'] * custom_lending['size']
            # st.write(custom_lending)
            # aaa = px.line(custom_lending,x='time',y='rate',render_mode="SVG")
            # st.plotly_chart(aaa)
            custom_lending['rate_bps_hr'] = custom_lending['rate'] * 1000
            custom_lending['accumulated']  = (list(accumulate(custom_lending['rate_bps_hr'])))
            window = 20
            no_of_std = 2
            def bollinger_strat(custom_lending, window, no_of_std):
                rolling_mean = custom_lending['rateAPY'].rolling(window).mean()
                rolling_std = custom_lending['rateAPY'].rolling(window).std()
                custom_lending['rolling_mean'] = rolling_mean

                custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
                custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
                return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
            bollinger_strat(custom_lending,window,no_of_std)
            bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','rateAPY','rolling_mean'],render_mode="SVG")
            # st.plotly_chart(bbbbbbb, use_container_width=True)



            def bollinger_strat(custom_lending, window, no_of_std):
                rolling_mean = custom_lending['size'].rolling(window).mean()
                rolling_std = custom_lending['size'].rolling(window).std()
                custom_lending['rolling_mean'] = rolling_mean

                custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
                custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
                return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
            bollinger_strat(custom_lending,window,no_of_std)
            bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','size','rolling_mean'],render_mode="SVG")
            # st.plotly_chart(bbbbbbb, use_container_width=True)


            def bollinger_strat(custom_lending, window, no_of_std):
                rolling_mean = custom_lending['accumulated'].rolling(window).mean()
                rolling_std = custom_lending['accumulated'].rolling(window).std()
                custom_lending['rolling_mean'] = rolling_mean

                custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
                custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
                return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
            bollinger_strat(custom_lending,window,no_of_std)
            bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','accumulated','rolling_mean'],render_mode="SVG")
            # st.plotly_chart(bbbbbbb, use_container_width=True)


            def bollinger_strat(custom_lending, window, no_of_std):
                rolling_mean = custom_lending['interest'].rolling(window).mean()
                rolling_std = custom_lending['interest'].rolling(window).std()
                custom_lending['rolling_mean'] = rolling_mean

                custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
                custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
                return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
            bollinger_strat(custom_lending,window,no_of_std)
            bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','interest','rolling_mean'],render_mode="SVG")
            # st.plotly_chart(bbbbbbb, use_container_width=True)


            def bollinger_strat(custom_lending, window, no_of_std):
                rolling_mean = custom_lending['rate_bps_hr'].rolling(window).mean()
                rolling_std = custom_lending['rate_bps_hr'].rolling(window).std()
                custom_lending['rolling_mean'] = rolling_mean

                custom_lending['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
                custom_lending['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
                return custom_lending['Bollinger High'] , custom_lending['Bollinger Low'], custom_lending['rolling_mean'] 
            bollinger_strat(custom_lending,window,no_of_std)
            bbbbbbb = px.line(custom_lending,x='time',y=['Bollinger High','Bollinger Low','rate_bps_hr','rolling_mean'],render_mode="SVG")
            # st.plotly_chart(bbbbbbb, use_container_width=True)

            latest_rateAPY_spot = custom_lending['rateAPY'].iloc[-1]
            # st.write("Latest Funding rate APY", latest_rateAPY_spot)
            latest_rate_bps_hr_spot = custom_lending['rate'].iloc[-1]
            # st.write("latest_rate_bps_hr_spot", latest_rate_bps_hr_spot)
        #     return latest_rateAPY_spot, latest_rate_bps_hr_spot
        # return latest_rateAPY_spot, latest_rate_bps_hr_spot
    else:
        custom_lending['rate'] = 0.00000000001
        custom_lending['rateAPY'] = 0.00000000001

        latest_rateAPY_spot = 0.0000000001
        # custom_lending['rateAPY'].iloc[-1] = 0.0000000001
        latest_rateAPY_spot = 0.00000000001
        # st.write("latest rate APY", latest_rateAPY_spot)
        latest_rate_bps_hr_spot = 0.000000000001
        # st.write("rate_bps_hr", latest_rate_bps_hr_spot)
    # return latest_rateAPY_spot, latest_rate_bps_hr
        # continue
    # return latest_rateAPY_spot, latest_rate_bps_hr





    # st.write('hourly funding rate in basis points')
    # bbbbbb = px.line(custom_lending,x='time',y='rate_bps_hr',render_mode="SVG")
    # st.plotly_chart(bbbbbb, use_container_width=True)
    # bbbbbbb = px.line(custom_lending,x='time',y='accumulated',render_mode="SVG")
    # st.plotly_chart(bbbbbbb, use_container_width=True)






    # st.write(name_perp)
    # st.title('perpetual futures')



    df = requests.get(f"https://ftx.com/api/markets/{name_perp}/candles?resolution=14400").json()
    # st.write(df)
    df = pd.DataFrame(df['result'])

    # st.write(df)
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                row_width=[0.2, 0.7])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df['startTime'],open=df['open'], high=df['high'],low=df['low'], close=df['close'],name="OHLC"), row=1, col=1)

    # include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['startTime'], y=df['volume'],
                showlegend=False), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    # st.plotly_chart(fig, use_container_width=True)















    df30 = requests.get(f"https://ftx.com/api/markets/{name_perp}/orderbook?depth=100").json()
    df30 = pd.DataFrame(df30)
    df30 = df30['result']
    asks = df30['asks']
    bids = df30['bids']
    # rename collums
    # plot depth
    # pick orders
    # pragnate orders into ccxt
    # exec


    # loop later to show postioning
    asks = pd.DataFrame(asks)
    bids = pd.DataFrame(bids)
    # st.write(df1)


    asks = asks.rename(columns={0: "price", 1: "size"})
    bids = bids.rename(columns={0: "price", 1: "size"})
    asks['accumulated']  = (list(accumulate(asks['size'])))
    asks['accumulated_price']  = (asks['price']) * asks['size']
    asks['accumulated_avg_price'] = (list(accumulate(asks['accumulated_price'])))  / asks['accumulated']
    asks['cash_equivelant'] = asks['accumulated'] * asks['accumulated_avg_price']


    bids['accumulated']  = (list(accumulate(bids['size'])))
    bids['accumulated_price']  = (bids['price']) * bids['size']
    bids['accumulated_avg_price'] = (list(accumulate(bids['accumulated_price'])))  / bids['accumulated']
    bids['cash_equivelant'] = bids['accumulated'] * bids['accumulated_avg_price']

    now = datetime.now()
    next_hour = now + timedelta(hours=1)
    # st.write(now)
    # st.write(next_hour)
    date = datetime.strptime(str(next_hour), '%Y-%m-%d %H:%M:%S.%f')
    newdate = date.replace(minute=0,second=0)
    # newdate = date.replace(second=0)

    # st.write(date)
    # st.write(newdate)
    time_till_expiry = newdate - now
    # st.write("time till expiry", time_till_expiry)

    pct_expiry = (time_till_expiry.total_seconds() / 3600) / 24 / 365.24 * 100
    # st.write("percentage till expiry", pct_expiry, "%")


    # st.write(hour)
    # expiry = pd.to_datetime(hour, format='%m%d')
    # st.write(expiry)
    column = bids["price"]
    max_value_perps = column.max()
    # st.write("best bid perps", max_value_perps)


    column = asks["price"]
    min_value_perps = column.min()
    # st.write("best bid asks", min_value_perps)

    spred_perps = min_value_perps - max_value_perps
    # st.write("perp spread",spred_perps)

    spred_bps_perps = spred_perps/min_value_perps*1000
    # st.write("perp spread", spred_bps_perps , "bps")
    # asks['price'] = asks[0]
    # asks['size'] = asks[1]
    # for i in range(1, 2):
    #     cols = st.columns(2)
    #     cols[0].subheader('bids')

    #     cols[0].write(bids)
    #     cols[1].subheader('asks')
        
    #     cols[1].write(asks)



    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(

        go.Scatter(x=asks['price'], y=asks['accumulated'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['price'], y=bids['accumulated'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)




    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=asks['price'], y=asks['size'], name="asks"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(x=bids['price'], y=bids['size'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="orderbook"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=asks['accumulated_avg_price'], y=asks['cash_equivelant'], name="asks"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=bids['accumulated_avg_price'], y=bids['cash_equivelant'], name="bids"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="cash_equivelant"
    )

    # Set x-axis title


    # st.plotly_chart(fig, use_container_width=True)
    # st.write("Predicted funding rate. Longs pay shorts if positive, shorts pay longs if negative. 1/24 times the average premium over the hour.")
    custom = requests.get(f"https://ftxpremiums.com/assets/data/funding_data/{name_perp}.json").json()




    custom = pd.DataFrame(custom)
    custom['rate'] = custom['rate'].astype(float)
    custom['time'] =  pd.to_datetime(custom['time'], unit='s')
    custom = custom.sort_values(by="time")

    custom['rate'] = custom['rate'] * 1000
    custom['rate_APY'] = custom['rate'] / 10 * 24 * 365.24

    custom['accumulated']  = (list(accumulate(custom['rate'])))
    # / 10 * 24 * 365.24




    window = 20
    no_of_std = 2



    def bollinger_strat(custom, window, no_of_std):
        rolling_mean = custom['rate_APY'].rolling(window).mean()
        rolling_std = custom['rate_APY'].rolling(window).std()
        custom['rolling_mean_rate_APY'] = rolling_mean

        custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
        custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
        return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean_rate_APY'] 
    bollinger_strat(custom,window,no_of_std)
    bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','rate_APY','rolling_mean_rate_APY'],render_mode="SVG")
    # st.plotly_chart(bbbbbbb, use_container_width=True)




    # st.write('hourly funding rate in basis points')


    def bollinger_strat(custom, window, no_of_std):
        rolling_mean = custom['rate'].rolling(window).mean()
        rolling_std = custom['rate'].rolling(window).std()
        custom['rolling_mean_rate'] = rolling_mean

        custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
        custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
        return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean_rate'] 
    bollinger_strat(custom,window,no_of_std)
    bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','rate','rolling_mean_rate'],render_mode="SVG")
    # st.plotly_chart(bbbbbbb, use_container_width=True)


    def bollinger_strat(custom, window, no_of_std):
        rolling_mean = custom['accumulated'].rolling(window).mean()
        rolling_std = custom['accumulated'].rolling(window).std()
        custom['rolling_mean_accumulated'] = rolling_mean

        custom['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
        custom['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)     
        return custom['Bollinger High'] , custom['Bollinger Low'], custom['rolling_mean_accumulated'] 
    bollinger_strat(custom,window,no_of_std)
    bbbbbbb = px.line(custom,x='time',y=['Bollinger High','Bollinger Low','accumulated','rolling_mean_accumulated'],render_mode="SVG")
    # st.plotly_chart(bbbbbbb, use_container_width=True)







    # try and do rolling average and rolling stddev











    # st.title("misc")
    # st.write("dated:",names_premeiums)
    # st.write("spot:",names_lending)
    # st.write("perp:", name_perp)
    numbers = len(names_lending)
    # st.write(numbers)
    # """verify that names_premiums, names_lending, name_perp are the same asset by looking at the fist 4 letters"""
    def spelling(numbers, names_premiums, names_lending, name_perp):
        if names_premiums[:numbers] == names_lending[:numbers] and names_premiums[:numbers] == name_perp[:numbers]:
            return True
        else:
            return False
    a = spelling(numbers, names_premeiums, names_lending, name_perp)
    # st.write("are the assets the same?",a)
    # st.subheader("dated futures")
    # st.write("best bid dated futures", max_value_dated_futures)
    # st.write("best ask dated futures", min_value_dated_futures)
    # st.write("spread dated futures", spred_dated)
    # st.write("spread dated futures", spred_dated_BPS, "bps")
    # st.write("expiry date", expiry)
    # st.write("now",datetime.now())
    # st.write("days until expiry: ", days_until_expiry)
    # st.write("expiry time - pct of a year: ", pct_expiry_dated, "%")


    # st.subheader("lending/spot")
    # latest_rateAPY_spot = custom_lending['rateAPY'].iloc[-1]
    # st.write("latest rate APY", latest_rateAPY_spot)
    # # latest_rate_bps_hr = custom_lending['rate_bps_hr'].iloc[-1]
    # st.write("rate_bps_hr", latest_rate_bps_hr_spot)
    # st.write("now",datetime.now())
    # st.write("best bid", max_value_spot)
    # st.write("best ask", min_value_spot)
    # st.write("spot spread", spred_spot)
    # st.write("spred_bps", spred_bps_spot , "bps")





    # st.subheader("funding/perpetual")
    latest_rateAPY = custom['rate_APY'].iloc[-1]
    # st.write("Latest Funding rate APY", latest_rateAPY)
    latest_rate_bps_hr = custom['rate'].iloc[-1]
    # st.write("funding_rate_bps_hr", latest_rate_bps_hr)
    rolling_mean_funding = custom['rolling_mean_rate_APY'].iloc[-1]
    # st.write("rolling_mean_funding", rolling_mean_funding)
    # st.write("time till expiry", time_till_expiry)
    # st.write("percentage till expiry", pct_expiry, "%")
    # st.write("best bid perps", max_value_perps)
    # st.write("best bid asks", min_value_perps)
    # st.write("perp spread",spred_perps)
    # st.write("perp spread", spred_bps_perps , "bps")


    # st.subheader("""first we look at spot vs dated """)

    long_spot_position_to_expiry = (min_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_dated/100))))
    short_spot_position_to_expiry = (max_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry_dated/100))))

    PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE = (max_value_dated_futures - long_spot_position_to_expiry) 
    PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE = (short_spot_position_to_expiry - min_value_dated_futures) 

    PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY = PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE / (min_value_spot * (pct_expiry_dated/100)) * 100
    PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE_APY = PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE / (max_value_spot * (pct_expiry_dated/100)) * 100

    # st.write("buy", min_value_spot, "spot", "sell", max_value_dated_futures, "dated_future")
    # st.write("long_spot_position_to_expiry",long_spot_position_to_expiry)
    # st.write("PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE",PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE)
    # st.write(PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY, "% APY")





    # st.write("sell", max_value_spot, "spot", "buy", min_value_dated_futures, "dated_future")
    # st.write("short_spot_position_to_expiry",short_spot_position_to_expiry)
    # st.write("PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE",PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE)
    # st.write(PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE, "% APY")


    # st.subheader("""next we look at spot vs perp""")


    spot_long_spot_position_to_expiry_perp = (min_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry/100))))
    spot_short_spot_position_to_expiry_perp = (max_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry/100))))

    perp_long_spot_position_to_expiry_perp = (max_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry/100))))
    perp_short_spot_position_to_expiry_perp = (min_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry/100))))

    PREMIUM_LONG_SPOT_SHORT_PERP = (perp_long_spot_position_to_expiry_perp - spot_long_spot_position_to_expiry_perp) 
    PREMIUM_SHORT_SPOT_LONG_PERP = (spot_short_spot_position_to_expiry_perp - perp_short_spot_position_to_expiry_perp)


    PREMIUM_LONG_SPOT_SHORT_PERP_APY = PREMIUM_LONG_SPOT_SHORT_PERP / (min_value_spot * (pct_expiry/100)) * 100
    PREMIUM_SHORT_SPOT_LONG_PERP_APY = PREMIUM_SHORT_SPOT_LONG_PERP / (max_value_spot * (pct_expiry/100)) * 100



    # st.write("sell PERP @ ", max_value_perps, "buy spot @ ", min_value_spot)
    # st.write("long_spot_position_to_expiry",spot_long_spot_position_to_expiry_perp)
    # st.write("perp_long_spot_position_to_expiry_perp",perp_long_spot_position_to_expiry_perp)
    # st.write("PREMIUM_LONG_SPOT_SHORT_PERP",PREMIUM_LONG_SPOT_SHORT_PERP)
    # st.write(PREMIUM_LONG_SPOT_SHORT_PERP_APY, "% APY")

    # st.write("sell spot @ ", max_value_spot, "buy perp @ ", min_value_perps)
    # st.write("short_spot_position_to_expiry",spot_short_spot_position_to_expiry_perp)
    # st.write("perp_short_spot_position_to_expiry_perp",perp_short_spot_position_to_expiry_perp)
    # st.write("PREMIUM_SHORT_SPOT_LONG_PERP",PREMIUM_SHORT_SPOT_LONG_PERP)
    # st.write(PREMIUM_SHORT_SPOT_LONG_PERP_APY, "% APY")

    # st.subheader("now dated_futures vs perps")


    long_perp_position_to_expiry = (min_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_dated/100))))
    short_perp_position_to_expiry = (max_value_perps * (1 + ((latest_rateAPY/1000)*(pct_expiry_dated/100))))

    PREMIUM_LONG_PERP_SHORT_DATED_FUTURE = (max_value_dated_futures - long_perp_position_to_expiry) 
    PREMIUM_SHORT_PERP_LONG_DATED_FUTURE = (short_perp_position_to_expiry - min_value_dated_futures) 

    PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY = PREMIUM_LONG_PERP_SHORT_DATED_FUTURE / (min_value_perps * (pct_expiry_dated/100)) * 100
    PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY = PREMIUM_SHORT_PERP_LONG_DATED_FUTURE / (max_value_perps * (pct_expiry_dated/100)) * 100




    # st.write("buy", min_value_perps, "perp", "sell", max_value_dated_futures, "dated_future")
    # st.write("long_perp_position_to_expiry",long_perp_position_to_expiry)
    # st.write("PREMIUM_LONG_PERP_SHORT_DATED_FUTURE",PREMIUM_LONG_PERP_SHORT_DATED_FUTURE)
    # st.write(PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY, "% APY")





    # st.write("sell", max_value_perps, "perp", "buy", min_value_dated_futures, "dated_future")
    # st.write("short_perp_position_to_expiry",short_perp_position_to_expiry)
    # st.write("PREMIUM_SHORT_PERP_LONG_DATED_FUTURE",PREMIUM_SHORT_PERP_LONG_DATED_FUTURE)
    # st.write(PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY, "% APY")





    # st.subheader("""next we look at spot vs perp rolling mean""")


    # spot_long_spot_position_to_expiry_perp = (min_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry/100))))
    # spot_short_spot_position_to_expiry_perp = (max_value_spot * (1 - ((latest_rateAPY_spot/1000)*(pct_expiry/100))))

    # perp_long_spot_position_to_expiry_perp = (max_value_perps * (1 + ((rolling_mean_funding/1000)*(pct_expiry/100))))
    # perp_short_spot_position_to_expiry_perp = (min_value_perps * (1 + ((rolling_mean_funding/1000)*(pct_expiry/100))))

    # PREMIUM_LONG_SPOT_SHORT_PERP = (perp_long_spot_position_to_expiry_perp - spot_long_spot_position_to_expiry_perp) 
    # PREMIUM_SHORT_SPOT_LONG_PERP = (spot_short_spot_position_to_expiry_perp - perp_short_spot_position_to_expiry_perp)


    # PREMIUM_LONG_SPOT_SHORT_PERP_APY = PREMIUM_LONG_SPOT_SHORT_PERP / (min_value_spot * (pct_expiry/100)) * 100
    # PREMIUM_SHORT_SPOT_LONG_PERP_APY = PREMIUM_SHORT_SPOT_LONG_PERP / (max_value_spot * (pct_expiry/100)) * 100



    # # st.write("sell PERP @ ", max_value_perps, "buy spot @ ", min_value_spot)
    # # st.write("long_spot_position_to_expiry",spot_long_spot_position_to_expiry_perp)
    # # st.write("perp_long_spot_position_to_expiry_perp",perp_long_spot_position_to_expiry_perp)
    # # st.write("PREMIUM_LONG_SPOT_SHORT_PERP",PREMIUM_LONG_SPOT_SHORT_PERP)
    # # st.write(PREMIUM_LONG_SPOT_SHORT_PERP_APY, "% APY")

    # # st.write("sell spot @ ", max_value_spot, "buy perp @ ", min_value_perps)
    # # st.write("short_spot_position_to_expiry",spot_short_spot_position_to_expiry_perp)
    # # st.write("perp_short_spot_position_to_expiry_perp",perp_short_spot_position_to_expiry_perp)
    # # st.write("PREMIUM_SHORT_SPOT_LONG_PERP",PREMIUM_SHORT_SPOT_LONG_PERP)
    # # st.write(PREMIUM_SHORT_SPOT_LONG_PERP_APY, "% APY")

    # # st.subheader("now dated_futures vs perps rolling mean")


    # long_perp_position_to_expiry = (min_value_perps * (1 + ((rolling_mean_funding/1000)*(pct_expiry_dated/100))))
    # short_perp_position_to_expiry = (max_value_perps * (1 + ((rolling_mean_funding/1000)*(pct_expiry_dated/100))))

    # PREMIUM_LONG_PERP_SHORT_DATED_FUTURE = (max_value_dated_futures - long_perp_position_to_expiry) 
    # PREMIUM_SHORT_PERP_LONG_DATED_FUTURE = (short_perp_position_to_expiry - min_value_dated_futures) 

    # PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY = PREMIUM_LONG_PERP_SHORT_DATED_FUTURE / (min_value_perps * (pct_expiry_dated/100)) * 100
    # PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY = PREMIUM_SHORT_PERP_LONG_DATED_FUTURE / (max_value_perps * (pct_expiry_dated/100)) * 100




    # st.write("buy", min_value_perps, "perp", "sell", max_value_dated_futures, "dated_future")
    # st.write("long_perp_position_to_expiry",long_perp_position_to_expiry)
    # st.write("PREMIUM_LONG_PERP_SHORT_DATED_FUTURE",PREMIUM_LONG_PERP_SHORT_DATED_FUTURE)
    # st.write(PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY, "% APY")





    # st.write("sell", max_value_perps, "perp", "buy", min_value_dated_futures, "dated_future")
    # st.write("short_perp_position_to_expiry",short_perp_position_to_expiry)
    # st.write("PREMIUM_SHORT_PERP_LONG_DATED_FUTURE",PREMIUM_SHORT_PERP_LONG_DATED_FUTURE)
    # st.write(PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY, "% APY")

    cash_n_carrydf.loc[i] = [i,lending,PREMIUM_LONG_SPOT_SHORT_DATED_FUTURE_APY,PREMIUM_SHORT_SPOT_LONG_DATED_FUTURE_APY, PREMIUM_LONG_SPOT_SHORT_PERP_APY, PREMIUM_SHORT_SPOT_LONG_PERP_APY,PREMIUM_LONG_PERP_SHORT_DATED_FUTURE_APY,PREMIUM_SHORT_PERP_LONG_DATED_FUTURE_APY]
    i = i + 1
    st.write(i)
    # st.write(cash_n_carrydf)


    # time.sleep(3)
# """previous formula has to be accrued hourly not daily """


# """verify the profitavilty of the cash and carry"""

# """first we look at spot vs dated """


# """next we look at spot vs perp """
st.write(cash_n_carrydf)
# """third we look at dated vs perp """
