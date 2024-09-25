import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import timedelta, datetime
import pandas_ta as ta
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

# Define a dictionary to store stock symbols and their display names
stock_options = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp",
    "NVDA": "NVIDIA Corporation",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms, Inc. Class A",
    "GOOGL": "Alphabet Inc. (Google) Class A",
    "BRK.B": "BERKSHIRE HATHAWAY Class B",
    "AVGO": "Broadcom Inc.",
    "GOOG": "Alphabet Inc. (Google) Class C",
    "LLY": "Eli Lilly & Co.",
    "BTC-USD":"Bitcoin Dollar",
    "SOL-USD":"Solana Dollar",
    "ETH-USD":"Ethereum Dollar",
    "DOGE-USD":"Doge Coin",
    "VOO":"sp500",
    # "INTC": "Intel",
    # "TSLA": "Tesla, Inc.",
    # "V": "Visa Inc.",
    # "NFLX": "Netflix Inc.",
    # "KO": "Coca Cola Company",
    # "MA": "Mastercard Incorporated",
    # "JPM": "Jpmorgan Chase & Co.",
    # "JNJ": "Johnson & Johnson",
    # "SBUX": "Starbucks",
}

# Get the list of stock names from the dictionary values
# stock_names = list(stock_options.values())

ini_time_for_now = datetime.now()
default_ticker = "VOO"

# Display a selection sidebar with stock names
st.sidebar.header("STOCKS:")
ticker = st.sidebar.selectbox("Ticker", stock_options)
ticker2 = st.sidebar.text_input("Benchmark", value="VOO")
start_date = st.sidebar.date_input("Begin datum", ini_time_for_now - timedelta(days=366))
end_date = st.sidebar.date_input("Eind datum")


col1, col2 = st.columns(2)

with col1:
    # Streamlit app setup
    st.subheader(f"Chart of {ticker}")
    # st.subheader(f'{ticker}')

    #Hiermee maken we de Chart en de Pricing data. waarbij we de input van de boxes in de sidebar gebruiken.
    data = yf.download(ticker, start=start_date, end=end_date)
    data3 = yf.download(ticker2, start=start_date, end=end_date)

    # last 24h % change
    latest_date = data.index[-1]
    previous_date = data.index[-2]
    latest_close = data.loc[latest_date, 'Close']
    previous_close = data.loc[previous_date, 'Close']
    price_change = latest_close - previous_close
    percent_change = (price_change / previous_close) * 100

    # Price change 24h
    if price_change > 0:
        st.metric(label=f"Price Change in Last 24 Hours", value=f"${latest_close:.2f}", delta=f"{percent_change:.2f}% ↑")
    else:
        st.metric(label=f"Price Change in Last 24 Hours", value=f"${latest_close:.2f}", delta=f"{percent_change:.2f}% ↓")

    # Create a candlestick trace
    trace = go.Candlestick(
        x=data.index,  # X-axis data (timestamps)
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
    )

    # Create the figure
    fig = go.Figure(data=[trace])  # Pass the list of traces

    st.plotly_chart(fig)

with col2:
    #tweede titel voor benchmark
    st.subheader(f"Benchmark {ticker2}")

# last 24h % change
    latest_date = data3.index[-1]
    previous_date = data3.index[-2]
    latest_close = data3.loc[latest_date, 'Close']
    previous_close = data3.loc[previous_date, 'Close']
    price_change = latest_close - previous_close
    percent_change = (price_change / previous_close) * 100

    # Price change 24h
    if price_change > 0:
        st.metric(label=f"Price Change in Last 24 Hours", value=f"${latest_close:.2f}", delta=f"{percent_change:.2f}% ↑")
    else:
        st.metric(label=f"Price Change in Last 24 Hours", value=f"${latest_close:.2f}", delta=f"{percent_change:.2f}% ↓")

    trace2 = go.Candlestick(
        x=data3.index,  # X-axis data (timestamps)
        open=data3["Open"],
        high=data3["High"],
        low=data3["Low"],
        close=data3["Close"],
    )

    fig2 = go.Figure(data=[trace2])  # Pass the list of traces


    st.plotly_chart(fig2)

# WIL EIGENLIJK HIER KORTE BESCHRIJVING VAN HET AANDEEL,
# ZO MOOI ONDER DE GRAFIEK.


# pricing_data, fundamental_data, news, tech_indicator = st.tabs(["Pricing Data","Fundamental Data", "Latest News", "Technical Analysis Dashboard"])
pricing_data, fundamental_data, tech_indicator, signals = st.tabs(
    ["Prijs Data", "Fundamental Data", "Technische Analyses", "Signalen"]
)

with pricing_data:
    st.header(f"Price Movements of {ticker}")
    st.write(
        "gebouwd met Yfinance. een package die werkt als een scraper van Yahoo Finance nadat de API van Yahoo Finance is afgebroken"
    )
    data2 = data
    data2["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace=True)
    # st.write(data2)
    annual_return = data2["% Change"].mean() * 252 * 100
    st.write("the annual return is", annual_return, "%")
    stdev = np.std(data2["% Change"]) * np.sqrt(252)
    st.write("Standard Deviation is ", stdev * 100, "%")
    st.write("Risk Adj return is ", annual_return / (stdev * 100))

# EIGENLIJK IN DE SIDEBAR KLEIN LIJSTJE MET STIJGERS EN DALERS, DAS OOK LEUK

# from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    st.header(f'Fundamentals of {ticker}')
    st.write('We zitten helaas met een max van 25 requests per dag dus om dit online te gebruiken is niet handig, Wij presenteren het wel werkend. Fundamentals van bedrijven gebruik je niet standaard maar het geeft een beter inzicht in de performance van een bedrijf.')
#     st.write('Hiervoor hebben we de API gebruikt! we gebruiken de API van alpha vantage, die via hun documentatie ook gerund kan worden als package met een key. door het op deze manier te doen minimaliseren we de requests.')
#     key = '2925PDFSJVVI2IRD'
#     fd = FundamentalData(key, output_format = 'pandas')
#     st.subheader('Balance Sheet')
#     balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
#     bs = balance_sheet.T[2:]
#     bs.columns = list(balance_sheet.T.iloc[0])
#     st.write(bs)
#     st.subheader('Income Statement')
#     income_statement = fd.get_income_statement_annual(ticker)[0]
#     is1 = income_statement.T[2:]
#     is1.collumns = list(income_statement.T.iloc[0])
#     st.write(is1)
#     st.subheader('Cash Flow Statement')
#     cash_flow = fd.get_cash_flow_annual(ticker)[0]
#     cf = cash_flow.T[2:]
#     cf.collumns = list(cash_flow.T.iloc[0])
#     st.write(cf)

with tech_indicator:
    st.subheader(f"Technicals {ticker}")
    df = pd.DataFrame()
    desired_indicators = ["sma", "swma", "rsi", "bbands", "macd", "ema"]

    ind_list = df.ta.indicators(as_list=True)
    tech_indicator = st.selectbox("Technical Indicators", options=desired_indicators)
    method = tech_indicator
    indicator = pd.DataFrame(
        getattr(ta, method)(
            low=data["Low"],
            close=data["Close"],
            high=data["High"],
            open=data["Open"],
            volume=data["Volume"],
        )
    )
    indicator["Close"] = data["Close"]
    figW_ind_new = px.line(indicator)
    st.plotly_chart(figW_ind_new)

with signals:
    st.write('Harstikke leuk dit allemaal maar we hebben allemaal dezelfde vraag moet ik nou kopen of verkopen...')
    st.write('Gebasseerd op de simple moving average met lengte 30 en 100 hebben we hier een grafiek')
   
    data['SMA 30'] = ta.sma(data['Close'],30)
    data['SMA 100'] = ta.sma(data['Close'],100)

    #SMA BUY SELL
    #Function for buy and sell signal
    def buy_sell(data):
        signalBuy = []
        signalSell = []
        position = False 

        for i in range(len(data)):
            if data['SMA 30'][i] > data['SMA 100'][i]:
                if position == False :
                    signalBuy.append(data['Adj Close'][i])
                    signalSell.append(np.nan)
                    position = True
                else:
                    signalBuy.append(np.nan)
                    signalSell.append(np.nan)
            elif data['SMA 30'][i] < data['SMA 100'][i]:
                if position == True:
                    signalBuy.append(np.nan)
                    signalSell.append(data['Adj Close'][i])
                    position = False
                else:
                    signalBuy.append(np.nan)
                    signalSell.append(np.nan)
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        return pd.Series([signalBuy, signalSell])

    data['Buy_Signal_price'], data['Sell_Signal_price'] = buy_sell(data)

    # Create a new figure object
    fig = go.Figure()

    # Plot the Adj Close price
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Adj Close'],
        name=ticker,
        mode='lines',
        line=dict(width=0.5, color='Grey', dash='solid')
    ))

    # Plot the SMA lines
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA 30'],
        name='SMA30',
        mode='lines',
        line=dict(width=0.5, color='orange', dash='longdash')
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA 100'],
        name='SMA100',
        mode='lines',
        line=dict(width=0.5, color='blue', dash='longdash')
    ))

    # Plot buy and sell signals as markers
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Buy_Signal_price'],
        mode='markers',
        name='Koop',
        marker=dict(
            symbol='triangle-up',
            size=12,  # Adjust marker size as needed
            color='green',
            opacity=1
        )
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Sell_Signal_price'],
        mode='markers',
        name='Verkoop',
        marker=dict(
            symbol='triangle-down',
            size=12,  # Adjust marker size as needed
            color='red',
            opacity=1
        )
    ))

    # Customize the layout
    fig.update_layout(
        title=ticker[0] + " Price History with Buy and Sell Signals",
        title_font_size=10,
        title_x=0.5,  # Center the title
        xaxis_title=f"{start_date} - {end_date}",
        xaxis_title_font_size=18,
        yaxis_title='Close Price',
        yaxis_title_font_size=18,
        legend_title_text='Signals'  # Add legend title
    )

    fig3 = fig

    # Show the plot
    # st.write('Signalen gebasseerd op SMA30 en SMA100')
    st.plotly_chart(fig3)
    

    st.write('Dat is een leuk begin, maar met enkele missers moeten we dat beter kunnen, dit is nog niet helemaal betrouwbaar. Misschien moeten we ook iets aan het risico management doen. Dat kan met MACD signialen, met stoploss op 2,5% voor risico management. De Moving Average Convergence of Divergence (oftewel MACD) is het verschil tussen 2 exponentiële Moving Averages.')
    #Strategy for signals
    macd = ta.macd(data['Close'])

    data = pd.concat([data, macd], axis=1).reindex(data.index)

    def MACD_Strategy(df, risk):
        MACD_Buy=[]
        MACD_Sell=[]
        position=False

        for i in range(0, len(df)):
            if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i] :
                MACD_Sell.append(np.nan)
                if position ==False:
                    MACD_Buy.append(df['Adj Close'][i])
                    position=True
                else:
                    MACD_Buy.append(np.nan)
            elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i] :
                MACD_Buy.append(np.nan)
                if position == True:
                    MACD_Sell.append(df['Adj Close'][i])
                    position=False
                else:
                    MACD_Sell.append(np.nan)
            elif position == True and df['Adj Close'][i] < MACD_Buy[-1] * (1 - risk):
                MACD_Sell.append(df["Adj Close"][i])
                MACD_Buy.append(np.nan)
                position = False
            elif position == True and df['Adj Close'][i] < df['Adj Close'][i - 1] * (1 - risk):
                MACD_Sell.append(df["Adj Close"][i])
                MACD_Buy.append(np.nan)
                position = False
            else:
                MACD_Buy.append(np.nan)
                MACD_Sell.append(np.nan)

        data['MACD_Buy_Signal_price'] = MACD_Buy
        data['MACD_Sell_Signal_price'] = MACD_Sell


    MACD_strategy = MACD_Strategy(data, 0.025)

    def MACD_color(data):
        MACD_color = []
        for i in range(0, len(data)):
            if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
                MACD_color.append(True)
            else:
                MACD_color.append(False)
        return MACD_color

    data['positive'] = MACD_color(data)


    colors = data.positive.map({True: 'green', False: 'red'})

    # Create subplots with appropriate dimensions
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Price plot on subplot 1
    price_trace = go.Scatter(
        x=data.index,
        y=data['Adj Close'],
        name='Close Price',
        mode='lines',
        line=dict(width=0.5, color='grey'),
    )
    signal_buy_trace = go.Scatter(
        x=data.index,
        y=data['MACD_Buy_Signal_price'],
        mode='markers',
        marker=dict(color='green', symbol='triangle-up', size=8),
    )
    signal_sell_trace = go.Scatter(
        x=data.index,
        y=data['MACD_Sell_Signal_price'],
        mode='markers',
        marker=dict(color='red', symbol='triangle-down', size=8),
    )
    fig.add_trace(price_trace, row=1, col=1)
    fig.add_trace(signal_buy_trace, row=1, col=1)
    fig.add_trace(signal_sell_trace, row=1, col=1)

    fig.update_layout(
        yaxis_title="Price in ₨",
        xaxis_title="Date",
        legend_title_text="Price",
        xaxis_tickformat="%Y-%m-%d",  # Adjust date format if needed
        margin=dict(t=30, l=30, r=20, b=20),
        showlegend=True,
    )

    # MACD plot on subplot 2
    macd_trace = go.Scatter(
        x=data.index,
        y=data['MACD_12_26_9'],
        name='MACD',
        mode='lines',
        line=dict(width=0.5, color='blue'),
    )
    macd_signal_trace = go.Scatter(
        x=data.index,
        y=data['MACDs_12_26_9'],
        name='Signal',
        mode='lines',
        line=dict(width=0.5, color='orange'),
    )
    macd_volume_trace = go.Bar(
        x=data.index,
        y=data['MACDh_12_26_9'],
        name='Volume',
        marker=dict(color=colors, opacity=0.8),
        width=0.8,
    )
    zero_line = go.Line(x=data.index, y=[0] * len(data), line=dict(color='black', width=0.5, dash='dash'))
    fig.add_trace(macd_trace, row=2, col=1)
    fig.add_trace(macd_signal_trace, row=2, col=1)
    fig.add_trace(macd_volume_trace, row=2, col=1)
    fig.add_trace(zero_line, row=2, col=1)

    fig.update_layout(
        yaxis2_title="MACD",
        legend_title_text="MACD",
        xaxis_tickformat="%Y-%m-%d",  # Adjust date format if needed
    )

    fig4 = fig

    st.plotly_chart(fig4)
