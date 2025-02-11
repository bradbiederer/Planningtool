import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Function to fetch census data (Replace with actual API or dataset source)
def get_census_data(geography, state=None, dma=None, race=None, language=None, income_range=None, house_value=None):
    # Mock data - Replace with real Census API integration
    data = {
        'ZIP Code': ['10001', '10002', '10003'],
        'Latitude': [40.7506, 40.7170, 40.7312],
        'Longitude': [-73.9970, -73.9857, -73.9935],
        'Population': [50000, 45000, 52000],
        'Median Household Income': ['$65,000', '$55,000', '$75,000'],
        'Median House Value': ['$500,000', '$450,000', '$600,000'],
        'Race': [race if race else 'All', race if race else 'All', race if race else 'All'],
        'Language Spoken': [language if language else 'All', language if language else 'All', language if language else 'All'],
        'Income Range': [income_range if income_range else 'All', income_range if income_range else 'All', income_range if income_range else 'All'],
        'House Value': [house_value if house_value else 'All', house_value if house_value else 'All', house_value if house_value else 'All']
    }
    return pd.DataFrame(data)

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
        st.dataframe(census_data[['ZIP Code', 'Population', 'Median Household Income', 'Median House Value']])
        
        # Allow selection of a ZIP code for mapping
        zip_selected = st.selectbox("Select a ZIP Code to visualize on map:", census_data['ZIP Code'])
        zip_info = census_data[census_data['ZIP Code'] == zip_selected].iloc[0]
        
        # Map Visualization
        m = folium.Map(location=[zip_info['Latitude'], zip_info['Longitude']], zoom_start=12)
        folium.Marker([zip_info['Latitude'], zip_info['Longitude']], tooltip="Selected ZIP Code", icon=folium.Icon(color='blue')).add_to(m)
        folium_static(m)

if __name__ == "__main__":
    main()
