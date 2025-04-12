import streamlit as st

st.set_page_config(page_title="Unit Converter", layout="centered")

# Apply Google-like styling
st.markdown("""
<style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .formula-box {
        background-color: #fef9e7;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 14px;
        margin-top: 10px;
        display: inline-block;
    }
    .formula-label {
        font-weight: bold;
        margin-right: 5px;
    }
    .stSelectbox {
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Unit conversion data structured by category
UNITS = {
    "Length": {
        "Nanometer": {"base": 1e-9},
        "Micrometer": {"base": 1e-6},
        "Millimeter": {"base": 1e-3},
        "Centimeter": {"base": 1e-2},
        "Inch": {"base": 0.0254},
        "Decimeter": {"base": 0.1},
        "Foot": {"base": 0.3048},
        "Yard": {"base": 0.9144},
        "Meter": {"base": 1.0},
        "Kilometer": {"base": 1000.0},
        "Mile": {"base": 1609.344},
        "Nautical mile": {"base": 1852.0},
        "Light year": {"base": 9.461e+15},
    },
    "Area": {
        "Square millimeter": {"base": 1e-6},
        "Square centimeter": {"base": 1e-4},
        "Square inch": {"base": 0.00064516},
        "Square foot": {"base": 0.09290304},
        "Square yard": {"base": 0.83612736},
        "Square meter": {"base": 1.0},
        "Acre": {"base": 4046.8564224},
        "Hectare": {"base": 10000.0},
        "Square kilometer": {"base": 1e+6},
        "Square mile": {"base": 2.59e+6},
    },
    "Volume": {
        "Milliliter": {"base": 1e-6},
        "Cubic centimeter": {"base": 1e-6},
        "Teaspoon (US)": {"base": 4.92892e-6},
        "Tablespoon (US)": {"base": 1.47868e-5},
        "Fluid ounce (US)": {"base": 2.95735e-5},
        "Cup (US)": {"base": 2.36588e-4},
        "Pint (US)": {"base": 4.73176e-4},
        "Quart (US)": {"base": 9.46353e-4},
        "Gallon (US)": {"base": 0.00378541},
        "Liter": {"base": 0.001},
        "Cubic meter": {"base": 1.0},
        "Cubic foot": {"base": 0.0283168},
        "Cubic yard": {"base": 0.764555},
    },
    "Weight": {
        "Microgram": {"base": 1e-9},
        "Milligram": {"base": 1e-6},
        "Gram": {"base": 0.001},
        "Ounce": {"base": 0.0283495},
        "Pound": {"base": 0.453592},
        "Kilogram": {"base": 1.0},
        "Stone": {"base": 6.35029},
        "US ton": {"base": 907.185},
        "Metric ton": {"base": 1000.0},
        "Imperial ton": {"base": 1016.05},
    },
    "Speed": {
        "Centimeter per second": {"base": 0.01},
        "Meter per second": {"base": 1.0},
        "Kilometer per hour": {"base": 0.277778},
        "Foot per second": {"base": 0.3048},
        "Mile per hour": {"base": 0.44704},
        "Knot": {"base": 0.514444},
        "Speed of light": {"base": 299792458.0},
    },
    "Time": {
        "Nanosecond": {"base": 1e-9},
        "Microsecond": {"base": 1e-6},
        "Millisecond": {"base": 0.001},
        "Second": {"base": 1.0},
        "Minute": {"base": 60.0},
        "Hour": {"base": 3600.0},
        "Day": {"base": 86400.0},
        "Week": {"base": 604800.0},
        "Month": {"base": 2.628e+6},
        "Year": {"base": 3.154e+7},
        "Decade": {"base": 3.154e+8},
        "Century": {"base": 3.154e+9},
    },
    "Temperature": {
        "Celsius": {"formula": lambda c: c, "inverse": lambda c: c},
        "Fahrenheit": {"formula": lambda c: c * 9/5 + 32, "inverse": lambda f: (f - 32) * 5/9},
        "Kelvin": {"formula": lambda c: c + 273.15, "inverse": lambda k: k - 273.15},
    },
    "Energy": {
        "Joule": {"base": 1.0},
        "Kilojoule": {"base": 1000.0},
        "Calorie": {"base": 4.184},
        "Kilocalorie": {"base": 4184.0},
        "Watt hour": {"base": 3600.0},
        "Kilowatt hour": {"base": 3.6e+6},
        "Electronvolt": {"base": 1.602e-19},
        "British thermal unit": {"base": 1055.06},
        "US therm": {"base": 1.055e+8},
        "Foot-pound": {"base": 1.35582},
    },
    "Pressure": {
        "Pascal": {"base": 1.0},
        "Kilopascal": {"base": 1000.0},
        "Bar": {"base": 100000.0},
        "Psi": {"base": 6894.76},
        "Atmosphere": {"base": 101325.0},
        "Torr": {"base": 133.322},
        "Millimeter of mercury": {"base": 133.322},
        "Inch of mercury": {"base": 3386.39},
    },
    "Data": {
        "Bit": {"base": 1/8},
        "Byte": {"base": 1.0},
        "Kilobit": {"base": 125.0},
        "Kilobyte": {"base": 1000.0},
        "Megabit": {"base": 125000.0},
        "Megabyte": {"base": 1e+6},
        "Gigabit": {"base": 1.25e+8},
        "Gigabyte": {"base": 1e+9},
        "Terabit": {"base": 1.25e+11},
        "Terabyte": {"base": 1e+12},
        "Petabit": {"base": 1.25e+14},
        "Petabyte": {"base": 1e+15},
    },
    "Angle": {
        "Degree": {"base": 1.0},
        "Radian": {"base": 57.2958},
        "Gradian": {"base": 0.9},
        "Milliradian": {"base": 0.0572958},
        "Minute of arc": {"base": 1/60},
        "Second of arc": {"base": 1/3600},
    },
    "Fuel Economy": {
        "Miles per gallon (US)": {"base": 1.0},
        "Miles per gallon (UK)": {"base": 1.20095},
        "Kilometer per liter": {"base": 0.425144},
        "Liter per 100 kilometers": {"inverse": True, "base": 235.215},
    },
    "Frequency": {
        "Hertz": {"base": 1.0},
        "Kilohertz": {"base": 1000.0},
        "Megahertz": {"base": 1e+6},
        "Gigahertz": {"base": 1e+9},
    },
    "Currency": {
        # Note: Currency rates would need to be updated regularly in a real app
        "USD": {"base": 1.0},
        "EUR": {"base": 0.92},
        "GBP": {"base": 0.77},
        "JPY": {"base": 150.55},
        "CAD": {"base": 1.37},
        "AUD": {"base": 1.52},
        "CHF": {"base": 0.90},
        "CNY": {"base": 7.23},
        "INR": {"base": 83.46},
    }
}

def convert_value(value, from_unit, to_unit, category):
    try:
        value = float(value)
        
        # Special case for temperature
        if category == "Temperature":
            # Convert from source unit to Celsius first
            celsius_value = UNITS[category][from_unit]["inverse"](value)
            # Then convert from Celsius to target unit
            return UNITS[category][to_unit]["formula"](celsius_value)
        
        # Special case for fuel economy with inverse relationship
        elif category == "Fuel Economy" and ("inverse" in UNITS[category][from_unit] or "inverse" in UNITS[category][to_unit]):
            if "inverse" in UNITS[category][from_unit] and "inverse" in UNITS[category][to_unit]:
                # Both are inverse (e.g., L/100km to L/100km)
                return value * UNITS[category][to_unit]["base"] / UNITS[category][from_unit]["base"]
            elif "inverse" in UNITS[category][from_unit]:
                # From inverse to normal (e.g., L/100km to mpg)
                return UNITS[category][to_unit]["base"] / (value / UNITS[category][from_unit]["base"])
            else:
                # From normal to inverse (e.g., mpg to L/100km)
                return UNITS[category][to_unit]["base"] / (value * UNITS[category][from_unit]["base"])
        
        # Normal case - convert using base unit
        else:
            # Convert from source unit to base unit
            base_value = value * UNITS[category][from_unit]["base"]
            # Convert from base unit to target unit
            return base_value / UNITS[category][to_unit]["base"]
            
    except (ValueError, TypeError):
        return None

def get_formula_text(from_unit, to_unit, category):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return "(°C x 9/5) + 32 = °F"
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return "°C + 273.15 = K"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return "(°F - 32) x 5/9 = °C"
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return "(°F - 32) x 5/9 + 273.15 = K"
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return "K - 273.15 = °C"
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return "(K - 273.15) x 9/5 + 32 = °F"
    
    # For same units
    if from_unit == to_unit:
        return f"value remains the same"
        
    # For currency
    if category == "Currency":
        return f"multiply the {from_unit} value by {UNITS[category][to_unit]['base']/UNITS[category][from_unit]['base']:.6g}"
    
    # Special case for fuel economy
    if category == "Fuel Economy":
        if "inverse" in UNITS[category][from_unit] and "inverse" not in UNITS[category][to_unit]:
            return f"divide {UNITS[category][to_unit]['base'] * UNITS[category][from_unit]['base']:.4g} by the value"
        elif "inverse" not in UNITS[category][from_unit] and "inverse" in UNITS[category][to_unit]:
            return f"divide {UNITS[category][to_unit]['base']:.4g} by the value"
    
    # Default case - calculate the conversion factor
    factor = UNITS[category][to_unit]["base"] / UNITS[category][from_unit]["base"]
    if factor >= 1:
        return f"multiply the {from_unit} value by {1/factor:.6g}" if factor < 1 else f"multiply the {from_unit} value by {factor:.6g}"
    else:
        return f"divide the {from_unit} value by {1/factor:.6g}"

# Main app layout
st.markdown('<p class="main-header">Unit Converter</p>', unsafe_allow_html=True)

# Unit selection
category = st.selectbox("Category", list(UNITS.keys()))

col1, col_equals, col2 = st.columns([2, 1, 2])

with col1:
    input_value = st.text_input("Input Value", value="1", key="input_value")
    from_unit = st.selectbox("From Unit", list(UNITS[category].keys()), key="from_unit")

with col_equals:
    st.markdown("<h1 style='text-align: center; margin-top: 20px;'>=</h1>", unsafe_allow_html=True)

with col2:
    to_unit = st.selectbox("To Unit", list(UNITS[category].keys()), key="to_unit")
    # Calculate and display result
    try:
        if input_value:
            result = convert_value(float(input_value), from_unit, to_unit, category)
            if result is not None:
                result_str = f"{result:.10g}"
                st.text_input("Result", value=result_str, key="result", disabled=True)
            else:
                st.text_input("Result", value="Invalid input", key="result", disabled=True)
        else:
            st.text_input("Result", value="", key="result", disabled=True)
    except:
        st.text_input("Result", value="Error", key="result", disabled=True)

# Formula display
formula_text = get_formula_text(from_unit, to_unit, category)
st.markdown(f'<div class="formula-box"><span class="formula-label">Formula:</span> {formula_text}</div>', unsafe_allow_html=True)

# Adding extra info about currency rates
if category == "Currency":
    st.info("Note: Currency rates are fixed for demo purposes. In a production app, these would be updated via API.")

# Footer
st.markdown("---")
st.markdown("Google-style Unit Converter - Built with Streamlit")