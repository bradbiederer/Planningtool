import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Title
st.title("Audience Planning Tool")

# Region selection
region_type = st.selectbox("Select Region Type", ["National", "State", "DMA"])

# User Inputs
income = st.text_input("Household Income ($)")
house_price = st.text_input("Average House Price ($)")
language = st.text_input("Language Spoken")

# Search button
if st.button("Find Zip Codes"):
    # Replace with your API or data source
    response = requests.post("https://your-api-endpoint.com/getZipCodes", json={
        "regionType": region_type,
        "filters": {"income": income, "housePrice": house_price, "language": language}
    })
    
    data = response.json()
    zip_codes = data.get("zipCodes", [])

    if zip_codes:
        st.success(f"Found {len(zip_codes)} matching Zip Codes!")
        st.write(zip_codes)
        
        # Map Visualization
        m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)  # USA Center
        for zip_code in zip_codes:
            # Fetch Lat/Long for Zip Code (Replace with your geolocation API)
            lat, lon = 37.7749, -122.4194  # Example coordinates (San Francisco)
            folium.Marker([lat, lon], popup=f"Zip: {zip_code}").add_to(m)

        folium_static(m)
    else:
        st.error("No matching zip codes found!")
