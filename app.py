import streamlit as st
import pandas as pd
import numpy as np

# --- Helper functions ---
def predict_from_unders(data, window=20, min_unders_for_above=10):
    if len(data) < window:
        return None, 0
    last_window = data[-window:]
    under_count = sum(1 for x in last_window if x < 2)  # assuming under = x < 2
    prediction = "Above" if under_count >= min_unders_for_above else "Under"
    return prediction, under_count

def bet_martingale(start_amount, last_result, last_bet):
    if last_result == "Lose":
        return last_bet * 2
    else:
        return start_amount

# --- Streamlit sidebar ---
st.sidebar.header("Settings")
min_unders = st.sidebar.number_input("Min unders for prediction (last 20)", value=10, min_value=1)
flat_bet = st.sidebar.number_input("Flat Bet Amount", value=1)
fixed_bet = st.sidebar.number_input("Fixed Bet Amount", value=2)
martingale_start = st.sidebar.number_input("Martingale Start Amount", value=1)

# --- Load data ---
@st.cache_data
def load_data():
    # replace this with your real crash data
    return np.random.randint(1, 6, size=200).tolist()  # random 1-5 for example

data = load_data()

# --- Predictions ---
st.subheader("Prediction from Under Count (last 20)")
prediction_20, under_count_20 = predict_from_unders(data, window=20, min_unders_for_above=min_unders)
if prediction_20:
    st.write(f"Prediction: **{prediction_20}** (Under count in last 20 = {under_count_20})")
else:
    st.write("Not enough data yet (need at least 20 rounds).")

st.subheader("Prediction from Under Count (last 50)")
prediction_50, under_count_50 = predict_from_unders(data, window=50, min_unders_for_above=int(min_unders * 50 / 20))
if prediction_50:
    st.write(f"Prediction: **{prediction_50}** (Under count in last 50 = {under_count_50})")
else:
    st.write("Not enough data yet (need at least 50 rounds).")

st.subheader("Prediction from Under Count (last 100)")
prediction_100, under_count_100 = predict_from_unders(data, window=100, min_unders_for_above=int(min_unders * 100 / 20))
if prediction_100:
    st.write(f"Prediction: **{prediction_100}** (Under count in last 100 = {under_count_100})")
else:
    st.write("Not enough data yet (need at least 100 rounds).")

# --- Betting Systems ---
st.subheader("Betting Systems")

# Flat
st.write(f"Flat Bet: ${flat_bet}")

# Fixed
st.write(f"Fixed Bet: ${fixed_bet}")

# Martingale
if 'last_martingale_bet' not in st.session_state:
    st.session_state.last_martingale_bet = martingale_start
if 'last_martingale_result' not in st.session_state:
    st.session_state.last_martingale_result = "Win"

next_martingale = bet_martingale(martingale_start, st.session_state.last_martingale_result, st.session_state.last_martingale_bet)
st.write(f"Martingale Bet: ${next_martingale}")
st.session_state.last_martingale_bet = next_martingale
