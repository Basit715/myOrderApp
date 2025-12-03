import streamlit as st
import pandas as pd
import os

# --- Page config ---
st.set_page_config(
    page_title="Fast Medicine Order App",
    page_icon="🟢",
    layout="wide"
)
st.title("⚡ Fast Medicine Order Entry — GitHub Excel Backend")

# --- File path ---
MYORDERS_FILE = "myorders.xlsx"

# --- Load / Save Orders ---
def load_orders():
    if os.path.exists(MYORDERS_FILE):
        try:
            df = pd.read_excel(MYORDERS_FILE, engine="openpyxl")
            return df.fillna("")
        except Exception as e:
            st.error(f"Error loading orders: {e}")
            return pd.DataFrame(columns=["Party Name","Medicine Name","Quantity"])
    else:
        return pd.DataFrame(columns=["Party Name","Medicine Name","Quantity"])

def save_orders(df):
    try:
        df.to_excel(MYORDERS_FILE, index=False, engine="openpyxl")
    except Exception as e:
        st.error(f"Error saving medicines: {e}")

# --- Load orders at startup ---
orders_df = load_orders()
if orders_df.empty:
    starting_entries = pd.DataFrame([
        {"Party Name":"Basit Medical store","Medicine Name":"Cyra D","Quantity":15}
    ])
    orders_df = pd.concat([orders_df, starting_entries], ignore_index=True)
    save_orders(orders_df)

# --- Session State ---
if 'current_party' not in st.session_state:
    st.session_state.current_party = ""
if 'current_order' not in st.session_state:
    st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])

# --- Party Name Input ---
party_name = st.text_input("Party Name", value=st.session_state.current_party, key="party_input")

# --- Add Medicine Form ---
with st.form("add_medicine_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        medicine_name = st.text_input("Medicine Name", key="medicine_input")
    with col2:
        quantity = st.number_input("Quantity", min_value=1, step=1, key="qty_input")
    with col3:
        submitted = st.form_submit_button("Add Medicine")
    
    if submitted:
        if party_name.strip() == "" or medicine_name.strip() == "":
            st.warning("Please enter both Party Name and Medicine Name!")
        else:
            st.session_state.current_party = party_name.strip()
            new_row = pd.DataFrame({'Medicine Name':[medicine_name.strip()],
                                    'Quantity':[quantity]})
            st.session_state.current_order = pd.concat([st.session_state.current_order, new_row], ignore_index=True)

# --- Show Current Order ---
st.subheader(f"Current Order for Party: {party_name}")
st.table(st.session_state.current_order)

# --- Buttons: Save / Export / Clear ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Save Order", key="save_order"):
        if st.session_state.current_order.empty:
            st.warning("Add medicines first!")
        else:
            order_to_save = st.session_state.current_order.copy()
            order_to_save.insert(0, 'Party Name', st.session_state.current_party)
            orders_df = pd.concat([orders_df, order_to_save], ignore_index=True)
            save_orders(orders_df)
            st.success(f"Order saved for {st.session_state.current_party}!")
            st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])

with col2:
    if st.button("Export All Orders to Excel", key="export_orders"):
        if orders_df.empty:
            st.warning("No orders to export!")
        else:
            orders_df.to_excel("medicine_orders.xlsx", index=False)
            st.success("All orders exported to medicine_orders.xlsx!")

with col3:
    if st.button("Clear Current Order", key="clear_order"):
        st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])
        st.session_state.current_party = ""
        st.success("Current order cleared!")

# --- Show All Orders Grouped by Party ---
st.subheader("All Orders (Grouped by Party)")

if orders_df.empty:
    st.info("No orders yet!")
else:
    grouped = orders_df.groupby("Party Name")
    for party, group in grouped:
        st.markdown(f"### {party}")
        st.table(group[['Medicine Name','Quantity']])
