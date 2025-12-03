import streamlit as st
import pandas as pd
import os

# --- SHOCKING CSS INJECTION ---
st.markdown(
    """
    <style>
    /* --- variables --- */
    :root{
      --bg1: #0b0f1a;
      --bg2: #0f0628;
      --neon1: #ff00cc; /* magenta */
      --neon2: #00fff2; /* cyan */
      --accent: #b8ff2e; /* lime */
      --glass: rgba(255,255,255,0.03);
      --panel-shadow: 0 8px 40px rgba(2,2,10,0.7);
      --glass-border: linear-gradient(120deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
      --flicker: drop-shadow(0 0 12px rgba(255,0,204,0.25)) drop-shadow(0 0 24px rgba(0,255,242,0.06));
    }

    /* --- animated gradient background --- */
    .stApp {
      background: radial-gradient(1200px 600px at 10% 10%, rgba(255,0,204,0.06), transparent 12%),
                  radial-gradient(900px 500px at 90% 85%, rgba(0,255,242,0.04), transparent 12%),
                  linear-gradient(120deg, var(--bg1), var(--bg2));
      min-height: 100vh;
      color: #e6f7ff;
      font-family: "Segoe UI", Roboto, system-ui, -apple-system, "Helvetica Neue", Arial;
      -webkit-font-smoothing: antialiased;
      animation: moveBg 18s linear infinite;
    }
    @keyframes moveBg {
      0% { background-position: 0% 0%, 100% 100%, 0% 0%;}
      50% { background-position: 10% 20%, 90% 80%, 100% 100%;}
      100% { background-position: 0% 0%, 100% 100%, 0% 0%;}
    }

    /* --- global headings --- */
    .stMarkdown h1, .stTitle, .stHeader, h1 {
      font-size: 2.25rem !important;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: white;
      text-shadow: 0 0 10px rgba(255,0,204,0.14), 0 0 30px rgba(0,255,242,0.06);
      border-left: 6px solid transparent;
      padding-left: 12px;
      margin-top: 6px;
      margin-bottom: 6px;
    }

    /* subtle neon flicker on the title */
    .stTitle{
      animation: neonFlicker 3.2s infinite;
    }
    @keyframes neonFlicker {
      0%, 19%, 21%, 23%, 100% { text-shadow: 0 0 30px var(--neon1), 0 0 40px var(--neon2); }
      20% { text-shadow: none; transform: translateY(-1px); }
      22% { text-shadow: 0 0 6px var(--neon2); transform: translateY(0); }
    }

    /* --- cards / main panels --- */
    .reportview-container .main, .stApp > .main, .block-container {
      padding: 1.5rem 2rem 3rem 2rem;
    }

    .stContainer, .element-container, .block-container .stBlock {
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.03);
      box-shadow: var(--panel-shadow);
      padding: 18px;
      margin-bottom: 14px;
      backdrop-filter: blur(6px) saturate(120%);
      transition: transform 0.35s cubic-bezier(.2,.9,.3,1), box-shadow 0.35s;
    }

    .stContainer:hover, .element-container:hover {
      transform: translateY(-6px);
      box-shadow: 0 20px 60px rgba(2,2,10,0.85);
    }

    /* --- form inputs --- */
    /* text input wrapper */
    div[role="textbox"], input[type="text"], textarea, .stTextInput > div > input {
      background: rgba(255,255,255,0.02) !important;
      border: 1px solid rgba(255,255,255,0.06) !important;
      color: #eaffff !important;
      padding: 10px 12px !important;
      border-radius: 10px !important;
      outline: none !important;
      box-shadow: 0 4px 18px rgba(0,0,0,0.6) inset;
    }

    /* number input & selects */
    input[type="number"], .stNumberInput > div > input {
      background: rgba(255,255,255,0.02) !important;
      border-radius: 10px !important;
      padding: 8px 10px !important;
      color: #f2fff7 !important;
    }

    /* labels / small text */
    .stMarkdown p, .stText, .stCaption {
      color: rgba(232, 250, 255, 0.95);
      font-weight: 600;
    }

    /* --- buttons --- */
    button[kind="primary"], .stButton>button {
      background: linear-gradient(90deg, var(--neon1), var(--neon2)) !important;
      border: none !important;
      color: #030312 !important;
      font-weight: 800 !important;
      padding: 10px 18px !important;
      border-radius: 12px !important;
      box-shadow: 0 6px 28px rgba(0,0,0,0.6), 0 0 22px rgba(255,0,204,0.12);
      transform: translateZ(0);
      transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .stButton>button:hover {
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 18px 40px rgba(0,0,0,0.7), 0 0 40px rgba(0,255,242,0.12);
    }
    .stButton>button:active {
      transform: translateY(-2px) scale(.995);
    }

    /* delete buttons (danger) */
    button[data-testid*="delete"], button[id*="delete"], .stButton>button[aria-label*="delete"] {
      background: linear-gradient(90deg, #ff2e6f, #ff8a00) !important;
      color: white !important;
      border-radius: 12px !important;
      box-shadow: 0 6px 24px rgba(255,46,111,0.14), 0 0 14px rgba(255,138,0,0.06);
    }

    /* export button - special outline */
    .export-button {
      border: 1px solid rgba(184,255,46,0.2);
      box-shadow: 0 8px 40px rgba(184,255,46,0.06);
    }

    /* --- tables --- */
    table {
      border-collapse: collapse !important;
      border-radius: 10px;
      overflow: hidden;
      width: 100%;
      background: linear-gradient(180deg, rgba(255,255,255,0.012), rgba(255,255,255,0.006));
      border: 1px solid rgba(255,255,255,0.03);
    }
    thead tr th {
      background: linear-gradient(90deg, rgba(255,0,204,0.06), rgba(0,255,242,0.04));
      color: white;
      font-weight: 800;
      padding: 10px;
      border-bottom: 1px solid rgba(255,255,255,0.03);
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    tbody tr td {
      padding: 9px;
      border-bottom: 1px dashed rgba(255,255,255,0.02);
      color: #eafcff;
      font-weight: 700;
    }
    tbody tr:hover td {
      transform: translateX(6px);
      transition: transform 0.25s ease;
      background: rgba(255,255,255,0.012);
    }

    /* badges and icons*/
    .party-badge {
      display:inline-block;
      padding:6px 10px;
      border-radius:999px;
      background: linear-gradient(90deg,var(--neon1),var(--neon2));
      color:#02020a;
      font-weight:800;
      box-shadow: 0 6px 24px rgba(0,0,0,0.5), 0 0 18px rgba(255,0,204,0.12);
      margin-bottom: 8px;
      margin-top:6px;
      letter-spacing:0.6px;
    }

    /* little neon underline under section headers */
    .stMarkdown h3, h3 {
      position: relative;
      color: #eaffff;
    }
    .stMarkdown h3:after, h3:after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -8px;
      width: 64px;
      height: 6px;
      background: linear-gradient(90deg, var(--neon1), var(--neon2));
      border-radius: 6px;
      box-shadow: 0 3px 18px rgba(255,0,204,0.12);
    }

    /* responsive tweaks for narrow screens */
    @media (max-width: 700px){
      .stContainer, .element-container { padding: 12px; border-radius: 10px; }
      .stTitle { font-size: 1.6rem !important; }
    }

    /* tiny animated accent dot next to party headers */
    .party-accent {
      height: 12px;
      width: 12px;
      border-radius: 50%;
      display:inline-block;
      margin-right:8px;
      background: conic-gradient(var(--neon1), var(--neon2));
      box-shadow: 0 0 12px rgba(255,0,204,0.35);
      animation: pulse 1.4s infinite;
      vertical-align: middle;
    }
    @keyframes pulse { 0% { transform: scale(.9); opacity:.9 } 50% { transform: scale(1.18); opacity:1 } 100% { transform: scale(.9); opacity:.9 } }

    /* small helpers to hide Streamlit footer and menu for maximum drama */
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Page config ---
st.set_page_config(
    page_title="Fast Medicine Order App",
    page_icon="🟢",
    layout="wide"
)

# --- App content continues below ---
st.title("⚡ My Order Entry Book - Tell Your Orders")

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
st.markdown(f"Current Order for Party: <span class='party-badge'><span class='party-accent'></span>{party_name}</span>", unsafe_allow_html=True)
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

# --- Show All Orders Grouped by Party With Delete Whole Party ---
st.subheader("All Orders (Grouped by Party)")

if orders_df.empty:
    st.info("No orders yet!")
else:
    grouped = orders_df.groupby("Party Name")

    for party, group in grouped:
        # display party header with neon badge
        st.markdown(f"<h3><span class='party-accent'></span>🔵 {party}</h3>", unsafe_allow_html=True)

        # Show medicines grouped
        st.table(group[['Medicine Name', 'Quantity']])

        # Delete entire order for this party
        if st.button(f"❌ Delete Entire Order for {party}", key=f"delete_{party}"):
            orders_df = orders_df[orders_df["Party Name"] != party]
            save_orders(orders_df)
            st.success(f"Deleted full order for {party}")
            st.rerun()
