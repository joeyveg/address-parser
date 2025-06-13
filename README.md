# Address Parser Web App (Fixed)

This app parses addresses using the Google Maps Geocoding API and outputs cleaned components like street, city, state, ZIP, and country.

## How to Run
```bash
pip install streamlit pandas openpyxl requests
streamlit run app.py
```

## Notes
- Make sure your Excel file has a column called `address_line1`
- This version fixes street address formatting to show: `123 Main St`