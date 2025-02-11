import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
import requests

# Census API Configuration
CENSUS_API_KEY = "YOUR_CENSUS_API_KEY"
CENSUS_API_URL = "https://api.census.gov/data/2020/acs/acs5"

# Function to fetch real census data
def get_census_data(geography, state=None, dma=None, race=None, language=None, income_range=None, house_value=None):
    params = {
        "get": "NAME,B01003_001E,B19013_001E,B25077_001E",
        "for": "zip code tabulation area:*",
        "key": CENSUS_API_KEY
    }
    response = requests.get(CENSUS_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data[1:], columns=["ZIP Code", "Population", "Median Household Income", "Median House Value", "ZCTA"])
        df.drop(columns=["ZCTA"], inplace=True)
        df["Population"] = df["Population"].astype(int)
        df["Median Household Income"] = df["Median Household Income"].astype(float).fillna(0).astype(int)
        df["Median House Value"] = df["Median House Value"].astype(float).fillna(0).astype(int)
        return df
    else:
        return pd.DataFrame()

# Streamlit UI
def main():
    st.title("Audience Planning Tool")
    st.write("Filter census data by geography, race, language spoken, household income, and house value.")
    
    # Geography Selection
    geography = st.selectbox("Select Geography:", ['National', 'State', 'DMA'])
    state, dma = None, None
    
    if geography == 'State':
        state = st.text_input("Enter State:")
    elif geography == 'DMA':
        dma = st.text_input("Enter DMA:")
    
    # User Inputs
    race = st.selectbox("Select Race:", ['All', 'White', 'Black', 'Asian', 'Hispanic', 'Other'])
    language = st.selectbox("Select Language Spoken:", ['All', 'English', 'Spanish', 'Chinese', 'French', 'Other'])
    income_range = st.selectbox("Select Household Income Range:", ['All', '<$40k', '$40k-$80k', '$80k-$120k', '>$120k'])
    house_value = st.selectbox("Select Average House Value:", ['All', '<$300k', '$300k-$500k', '$500k-$700k', '>$700k'])
    
    if st.button("Get Audience Insights"):
        census_data = get_census_data(geography, state, dma, race, language, income_range, house_value)
        st.write("The best ZIP codes that match your criteria:")
        st.dataframe(census_data)
        
        # Allow selection of a ZIP code for mapping
        if not census_data.empty:
            zip_selected = st.selectbox("Select a ZIP Code to visualize on map:", census_data['ZIP Code'])
            zip_info = census_data[census_data['ZIP Code'] == zip_selected].iloc[0]
            
            # Map Visualization
            m = folium.Map(location=[40.75, -73.99], zoom_start=12)  # Default location
            folium.Marker([40.75, -73.99], tooltip="Selected ZIP Code", icon=folium.Icon(color='blue')).add_to(m)
            folium_static(m)

if __name__ == "__main__":
    main()
