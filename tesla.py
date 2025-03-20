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
    fig.write_image("tesla_plot.png")


# Fetch Tesla stock price data
tesla = yf.Ticker("TSLA")
tesla_share_price_data = tesla.history(period="max")

# Reset the index to bring "Date" into its own column
tesla_share_price_data.reset_index(inplace=True)

print(tesla_share_price_data.head())

# Scrape revenue data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')

# Create an empty DataFrame
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Iterate through table rows in the second <tbody>
for row in soup.find_all("tbody")[1].find_all("tr"):  # Corrected iteration
    col = row.find_all("td")
    if len(col) >= 2:  # Ensure there are enough columns
        date = col[0].text.strip()
        revenue = col[1].text.strip()

        # Append data to DataFrame
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

# Clean the "Revenue" column by removing commas and dollar signs
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(r'[,\$]', '', regex=True)

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail(10))

make_graph(tesla_share_price_data, tesla_revenue, 'Tesla')

'''
apple_share_price_data = apple.history(period="max")
apple.dividends
apple.dividends.plot()
plt.show()
'''