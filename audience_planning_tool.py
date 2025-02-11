import streamlit as st
import folium
import pandas as pd
import requests
from streamlit_folium import folium_static

# Function to Fetch Publicly Available Data
@st.cache_data
def fetch_public_data():
    url = "https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/download/?format=csv"
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error("Failed to fetch ZIP code data. Please try again later.")
        return pd.DataFrame()  # Return an empty DataFrame to prevent app crashes

# Function to Fetch Nearby Businesses
def fetch_nearby_businesses(lat, lon, business_type):
    # Mock API call - Replace with actual data source like Google Places API
    business_data = {
        "Golf Courses": ["Golf Club A", "Golf Club B"],
        "Bars": ["Bar X", "Bar Y"],
        "Movie Theaters": ["Cinema 1", "Cinema 2"],
        "Banks": ["Bank A", "Bank B"],
        "Shopping Malls": ["Mall A", "Mall B"],
        "Quick Service Restaurants": ["Fast Food A", "Fast Food B"]
    }
    return business_data.get(business_type, [])

# Load Data
data = fetch_public_data()

# List of all states
states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

# List of DMAs (Example - Replace with real DMA data)
dma_list = ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco"]

# List of Languages
languages = ["English", "Spanish", "Chinese (Mandarin)", "Chinese (Cantonese)", "Japanese", "Tagalog", "Vietnamese", "Russian", "Ukrainian", "Korean", "Hindi"]

# Title
st.title("Audience Planning Tool")

# Region selection
region_type = st.selectbox("Select Region Type", ["National", "State", "DMA"])

# Conditional State Selection
if region_type == "State":
    selected_states = st.multiselect("Select State(s)", states)
else:
    selected_states = []

# Conditional DMA Selection
if region_type == "DMA":
    selected_dma = st.text_input("Enter DMA (start typing)")
    matched_dmas = [dma for dma in dma_list if selected_dma.lower() in dma.lower()]
    if matched_dmas:
        selected_dma = st.selectbox("Select DMA", matched_dmas)
else:
    selected_dma = ""

# User Inputs with Ranges
income_range = st.slider("Household Income Range ($)", 0, 500000, (50000, 150000), step=5000)
house_price_range = st.slider("Average House Price Range ($)", 0, 2000000, (200000, 800000), step=10000)
selected_languages = st.multiselect("Select Language(s) Spoken", languages)

# Search button
if st.button("Find Zip Codes"):
    if data.empty:
        st.error("No data available for processing.")
    else:
        filtered_data = data.copy()
        
        if selected_states:
            filtered_data = filtered_data[filtered_data["state"].isin(selected_states)]
        if selected_dma:
            filtered_data = filtered_data[filtered_data["dma"] == selected_dma]
        if income_range:
            filtered_data = filtered_data[(filtered_data["income"] >= income_range[0]) & (filtered_data["income"] <= income_range[1])]
        if house_price_range:
            filtered_data = filtered_data[(filtered_data["house_price"] >= house_price_range[0]) & (filtered_data["house_price"] <= house_price_range[1])]
        if selected_languages:
            filtered_data = filtered_data[filtered_data["language"].isin(selected_languages)]
        
        zip_codes = filtered_data["zip_code"].tolist()
        
        if zip_codes:
            st.success(f"Found {len(zip_codes)} matching Zip Codes!")
            st.write(zip_codes)
            
            # Display Language Indexing
            st.write("### Language Indexing in Suggested Zip Codes")
            language_counts = filtered_data["language"].value_counts()
            st.bar_chart(language_counts)
            
            # Map Visualization
            m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)  # USA Center
            for _, row in filtered_data.iterrows():
                folium.Marker([row["lat"], row["lon"]], popup=f"Zip: {row['zip_code']}").add_to(m)

            folium_static(m)
            
            # Business Search
            business_type = st.selectbox("Select Business Type", ["Golf Courses", "Bars", "Movie Theaters", "Banks", "Shopping Malls", "Quick Service Restaurants"])
            if st.button("Find Nearby Businesses"):
                for _, row in filtered_data.iterrows():
                    businesses = fetch_nearby_businesses(row["lat"], row["lon"], business_type)
                    st.write(f"Businesses near Zip {row['zip_code']}: {businesses}")
        else:
            st.error("No matching zip codes found!")
