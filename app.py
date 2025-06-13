import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Address Parser", layout="centered")
st.title("📍 Address Parser with Geocoding")

api_key = st.text_input("Enter your Google Maps Geocoding API Key", type="password")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file and api_key:
    df = pd.read_excel(uploaded_file)

    if 'address_line1' not in df.columns:
        st.error("The file must contain a column named 'address_line1'")
    else:
        st.info("Parsing addresses... this may take a minute.")

        def geocode(address):
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {"address": address, "key": api_key}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    components = {comp['types'][0]: comp['long_name'] for comp in data['results'][0]['address_components']}
                    return pd.Series({
                        'Street Address': components.get('street_number', '') + ' ' + components.get('route', ''),
                        'City': components.get('locality', '') or components.get('postal_town', ''),
                        'State/Department': components.get('administrative_area_level_1', ''),
                        'Zip Code': components.get('postal_code', ''),
                        'Country': components.get('country', '')
                    })
            return pd.Series({'Street Address': '', 'City': '', 'State/Department': '', 'Zip Code': '', 'Country': ''})

        parsed_df = df.copy()
        parsed_components = df['address_line1'].apply(geocode)
        parsed_df = pd.concat([parsed_df, parsed_components], axis=1)

        st.success("Finished parsing addresses!")

        buffer = io.BytesIO()
        parsed_df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="Download Cleaned Excel",
            data=buffer,
            file_name="parsed_addresses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )