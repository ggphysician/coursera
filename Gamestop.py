import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import webbrowser

#pio.renderers.default = "vscode"

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=0.3)

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)

    # Only show the graph without using Jupyter's display(HTML())
    fig.show()
    #webbrowser.open_new("http://localhost:8050")
    fig.write_image("gamestop_plot.png")

# Fetch gamestop stock price data
gamestop = yf.Ticker("GME")
gamestop_share_price_data = gamestop.history(period="max")

# Reset the index to bring "Date" into its own column
gamestop_share_price_data.reset_index(inplace=True)

print(gamestop_share_price_data.head())

# Scrape revenue data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text
soup = BeautifulSoup(html_data_2, 'html.parser')

# Create an empty DataFrame
gamestop_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Iterate through table rows in the second <tbody>
for row in soup.find_all("tbody")[1].find_all("tr"):  # Corrected iteration
    col = row.find_all("td")
    if len(col) >= 2:  # Ensure there are enough columns
        date = col[0].text.strip()
        revenue = col[1].text.strip()

        # Append data to DataFrame
        gamestop_revenue = pd.concat([gamestop_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

# Clean the "Revenue" column by removing commas and dollar signs
gamestop_revenue["Revenue"] = gamestop_revenue["Revenue"].str.replace(r'[,\$]', '', regex=True)

gamestop_revenue.dropna(inplace=True)

gamestop_revenue = gamestop_revenue[gamestop_revenue['Revenue'] != ""]

print(gamestop_revenue.tail())

make_graph(gamestop_share_price_data, gamestop_revenue, 'Gamestop')

