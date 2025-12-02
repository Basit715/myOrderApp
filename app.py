import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Fast Medicine Order App", layout="wide")
st.title("⚡ Fast Medicine Order Entry — Google Sheet Backend")

# --- Google Sheets Authentication ---
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

def read_excel_from_drive(file_id):
    service = gdrive_service()

    # Export Google Sheet to Excel
    data = service.files().export(
        fileId=file_id,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ).execute()

    buffer = io.BytesIO()
    buffer.write(data)
    buffer.seek(0)

    df = pd.read_excel(buffer, engine="openpyxl")
    return df
def write_excel_to_drive(df, file_id):
    service = gdrive_service()

    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine="openpyxl")
    excel_buffer.seek(0)

    media = MediaIoBaseUpload(
        excel_buffer,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=False
    )

    service.files().update(
        fileId=file_id,
        media_body=media
    ).execute()
MYORDERS_FILE = os.path.join(DATA_DIR, "myorders.xlsx")


# --- Session State ---
if 'current_party' not in st.session_state:
    st.session_state.current_party = ""
if 'current_order' not in st.session_state:
    st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])

# --- Party Name Input ---
party_name = st.text_input("Party Name", value=st.session_state.current_party)

# --- Add Medicine Form ---
with st.form("add_medicine_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([4,1,1])
    with col1:
        medicine_name = st.text_input("Medicine Name")
    with col2:
        quantity = st.number_input("Quantity", min_value=1, step=1)
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
    if st.button("Save Order",key = "save_order"):
        if st.session_state.current_order.empty:
            st.warning("Add medicines first!")
        elif sheet is None:
            st.error("Cannot save order: Google Sheet not accessible!")
        else:
            order_to_save = st.session_state.current_order.copy()
            order_to_save.insert(0, 'Party Name', st.session_state.current_party)
            order_list_df = pd.concat([order_list_df, order_to_save], ignore_index=True)
            # Update Google Sheet
            try:
                sheet.update([order_list_df.columns.values.tolist()] + order_list_df.values.tolist())
                st.success(f"Order saved for {st.session_state.current_party}!")
                st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])
            except Exception as e:
                st.error(f"Failed to update Google Sheet: {e}")

with col2:
    if st.button("Export All Orders to Excel",key = "export_orders"):
        if order_list_df.empty:
            st.warning("No orders to export!")
        else:
            order_list_df.to_excel("medicine_orders.xlsx", index=False)
            st.success("All orders exported to medicine_orders.xlsx!")

with col3:
    if st.button("Clear Current Order",key = "clear_order"):
        st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])
        st.session_state.current_party = ""
        st.success("Current order cleared!")

# --- Show All Orders ---
st.subheader("All Orders")
st.table(order_list_df)
st.subheader(f"Current Order for Party: {party_name}")
st.table(st.session_state.current_order)

# --- Buttons: Save / Export / Clear ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Save Order"):
        if st.session_state.current_order.empty:
            st.warning("Add medicines first!")
        else:
            order_to_save = st.session_state.current_order.copy()
            order_to_save.insert(0, 'Party Name', st.session_state.current_party)
            order_list_df = pd.concat([order_list_df, order_to_save], ignore_index=True)
            worksheet.update([order_list_df.columns.values.tolist()] + order_list_df.values.tolist())
            st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])
            st.success(f"Order saved for {st.session_state.current_party}!")

with col2:
    if st.button("Export All Orders to Excel"):
        if order_list_df.empty:
            st.warning("No orders to export!")
        else:
            order_list_df.to_excel("medicine_orders.xlsx", index=False)
            st.success("All orders exported to medicine_orders.xlsx!")

with col3:
    if st.button("Clear Current Order"):
        st.session_state.current_order = pd.DataFrame(columns=['Medicine Name', 'Quantity'])
        st.session_state.current_party = ""
        st.success("Current order cleared!")

# --- Display All Orders ---
st.subheader("All Orders")
st.table(order_list_df)
