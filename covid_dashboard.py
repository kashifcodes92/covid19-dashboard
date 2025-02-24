import pandas as pd
import requests
import streamlit as st
import plotly.express as px

# Function to fetch data from the API or fallback to static data
def fetch_data():
    try:
        # Try the COVID-19 API
        url = "https://api.covid19api.com/summary"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        df = pd.DataFrame(data['Countries'])
    except:
        # Fallback to static data if API fails
        df = pd.read_csv("covid_data.csv")
    return df

# Fetch data
df = fetch_data()

# Clean and process data
df = df[['Country', 'TotalConfirmed', 'TotalDeaths', 'TotalRecovered']]
df['RecoveryRate'] = (df['TotalRecovered'] / df['TotalConfirmed']) * 100
df['MortalityRate'] = (df['TotalDeaths'] / df['TotalConfirmed']) * 100
df.fillna(0, inplace=True)  # Handle missing values

# Visualize data with Plotly
# Bar chart: Top 10 countries by cases
fig1 = px.bar(df.nlargest(10, 'TotalConfirmed'), 
              x='Country', y='TotalConfirmed',
              title='Top 10 Countries by Total Cases')

# Scatter plot: Recovery vs. Mortality Rates
fig2 = px.scatter(df, x='MortalityRate', y='RecoveryRate',
                  hover_name='Country',
                  title='Recovery vs. Mortality Rates')

# Choropleth map: Global case distribution
fig3 = px.choropleth(df, locations='Country', locationmode='country names',
                     color='TotalConfirmed', title='Global Case Distribution')

# Build the Streamlit app
st.title("COVID-19 Data Dashboard")
st.write("Real-time data from COVID-19 API")

# Display global stats
st.subheader("Global Summary")
st.write(f"Total Cases: {df['TotalConfirmed'].sum():,}")
st.write(f"Total Deaths: {df['TotalDeaths'].sum():,}")
st.write(f"Total Recovered: {df['TotalRecovered'].sum():,}")

# Display charts
st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)

# Optional: Display raw data
if st.checkbox("Show Raw Data"):
    st.write(df)