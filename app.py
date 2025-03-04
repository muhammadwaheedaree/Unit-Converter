import streamlit as st
import pandas as pd

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Unit Converter Pro",
        page_icon="🔄",
        layout="centered"
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stSelectbox {
            margin-bottom: 1rem;
        }
        .converter-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .result-container {
            background-color: #e9ecef;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
        }
        .result-text {
            color: #495057;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title with emoji
    st.title("📐 Smart Unit Converter")
    st.markdown("---")

    # Initialize conversion factors dictionary
    conversion_factors = {
        "Length": {
            "Meters": 1.0,
            "Kilometers": 0.001,
            "Centimeters": 100,
            "Millimeters": 1000,
            "Miles": 0.000621371,
            "Yards": 1.09361,
            "Feet": 3.28084,
            "Inches": 39.3701
        },
        "Weight": {
            "Kilograms": 1.0,
            "Grams": 1000,
            "Milligrams": 1000000,
            "Pounds": 2.20462,
            "Ounces": 35.274,
            "Metric Tons": 0.001
        },
        "Temperature": {
            "Celsius": "C",
            "Fahrenheit": "F",
            "Kelvin": "K"
        }
    }

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        # Unit category selection
        category = st.selectbox("Select Category", list(conversion_factors.keys()))

    # Search functionality
    search_term = st.text_input("🔍 Search Units", "").lower()
    
    # Filter units based on search
    available_units = list(conversion_factors[category].keys())
    if search_term:
        available_units = [unit for unit in available_units if search_term in unit.lower()]
        if not available_units:
            st.warning("No units found matching your search.")
            return

    # Input and output unit selection
    col3, col4 = st.columns(2)
    
    with col3:
        from_unit = st.selectbox("From", available_units)
    
    with col4:
        to_unit = st.selectbox("To", available_units)

    # Input value
    input_value = st.number_input("Enter Value", value=0.0)

    # Conversion logic
    if st.button("Convert", type="primary"):
        try:
            if category == "Temperature":
                result = convert_temperature(input_value, from_unit, to_unit)
            else:
                result = convert_units(input_value, from_unit, to_unit, conversion_factors[category])
            
            # Display result with styling
            st.markdown(f"""
                <div style='background-color: #e9ecef; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
                    <h3 style='color: #495057; margin: 0;'>Result:</h3>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0; color: #495057;'>{input_value:.4g} {from_unit} = {result:.4g} {to_unit}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred during conversion: {str(e)}")

    # Add helpful information
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. Select the category of units you want to convert
        2. Use the search bar to filter units (optional)
        3. Choose the unit to convert from
        4. Choose the unit to convert to
        5. Enter the value you want to convert
        6. Click the 'Convert' button to see the result
        """)

def convert_temperature(value, from_unit, to_unit):
    # Temperature conversion logic
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Convert from Celsius to target unit
    if to_unit == "Fahrenheit":
        return (celsius * 9/5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius

def convert_units(value, from_unit, to_unit, factors):
    # Convert to base unit first, then to target unit
    base_value = value / factors[from_unit]
    return base_value * factors[to_unit]

if __name__ == "__main__":
    main()
