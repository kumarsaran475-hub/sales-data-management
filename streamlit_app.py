import streamlit as st
import pandas as pd
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "superadmin": {"password_hash": hash_password("May@2026"), "role": "Super Admin", "branch": None},
    "admin_chennai": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 1},
    "admin_banglore": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 2},
    "admin_hyderabad": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 3},
    "admin_delhi": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 4},
    "admin_mumbai": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 5},
    "admin_pune": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 6},
    "admin_kolkata": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 7},
    "admin_ahmedabad": {"password_hash": hash_password("Jun@2026"), "role": "Admin", "branch": 8}
}

def login(username, password):
    user = USERS.get(username)
    if user and user["password_hash"] == hash_password(password):
        return user
    return None

st.set_page_config(page_title="Customer Sales Dashboard", layout="wide")
st.title("📊 Customer Sales Dashboard")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome {username}! You are logged in as {user['role']}.")
        else:
            st.error("Invalid username or password")
else:
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    df = pd.read_csv(r"C:/Users/SARAN K/Downloads/customer_sales new.csv")

    if st.session_state.user["role"] == "Super Admin":
        pass  
    else:
        branch_id = st.session_state.user["branch"]
        df = df[df["branch_id"] == branch_id]
        st.sidebar.write(f"Branch Access: {branch_id}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        branch_filter = st.selectbox("Branch ID", options=["All"] + df["branch_id"].astype(str).unique().tolist())
    with col2:
        product_filter = st.selectbox("Product Name", options=["All"] + df["product_name"].unique().tolist())
    with col3:
        start_date = st.date_input("Start Date", value=None)
    with col4:
        end_date = st.date_input("End Date", value=None)

    
    filtered_df = df.copy()
    if branch_filter != "All":
        filtered_df = filtered_df[filtered_df["branch_id"].astype(str) == branch_filter]
    if product_filter != "All":
        filtered_df = filtered_df[filtered_df["product_name"] == product_filter]
    if start_date and end_date:
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df["start_date"], dayfirst=True) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_df["end_date"], dayfirst=True) <= pd.to_datetime(end_date))
        ]

    
    st.dataframe(filtered_df)

