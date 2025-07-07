import streamlit as st
import numpy as np
import pickle
import pandas as pd

# Load model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("📈 Stock Price Trend Prediction")

st.subheader("Enter today's stock data:")
open_val = st.number_input("Open Price")
high_val = st.number_input("High Price")
low_val = st.number_input("Low Price")
close_val = st.number_input("Close Price")
volume = st.number_input("Volume")

if 'prev_data' not in st.session_state:
    st.session_state['prev_data'] = []  

prev_close = st.session_state['prev_data'][0] if len(st.session_state['prev_data']) >= 1 else close_val
close_2_days_ago = st.session_state['prev_data'][1] if len(st.session_state['prev_data']) >= 2 else close_val
volume_lag = st.session_state['prev_data'][2] if len(st.session_state['prev_data']) >= 3 else volume
return_lag1 = st.session_state['prev_data'][3] if len(st.session_state['prev_data']) >= 4 else 0

# Calculate features
daily_return = ((close_val - open_val) / open_val) * 100 if open_val else 0
ma_3 = (open_val + high_val + low_val + close_val) / 4
ma_5 = (open_val + high_val + low_val + close_val + prev_close) / 5
ma_10 = ma_5  # Approximation (improve if you store last 10)

close_lag1 = prev_close
close_lag2 = close_2_days_ago

# Predict
if st.button("Predict Stock Trend"):
    try:
        input_data = np.array([[open_val, high_val, low_val, close_val, volume,
                                daily_return, ma_3, ma_5, ma_10,
                                close_lag1, close_lag2, volume_lag, return_lag1]])

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.success("Prediction: Price will go UP")
        else:
            st.warning("Prediction: Price will go DOWN")

        # Update session state
        st.session_state['prev_data'] = [close_val, close_lag1, volume, daily_return]

    except Exception as e:
        st.error(f"Error during prediction: {e}")