import streamlit as st
from datetime import  datetime
import requests
from dotenv import  load_dotenv
import  os

load_dotenv()

API_Url=os.getenv("API_Url")


def update_expense_tab():
    st.header("➕ Update Old Expense")
    selected_date = st.date_input("Enter Date to update expense", datetime.today())

    st.spinner("🔄 Loading expenses...")
    response=requests.get(f"{API_Url}/expenses/{selected_date}")

    if response.status_code==200:
        expenses=response.json()

        if not expenses:
            st.info(f"No expenses found for this date {selected_date}")
            return
    available_category = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    for idx, expense in enumerate(expenses):


        col1, col2, col3, col4 = st.columns([2, 2, 3, 2])

        record_key = f"{expense['id']}_{idx}"  # unique per row

        with col1:
            st.subheader("Amount")
            updated_amount = st.number_input(
                label="Amount",
                min_value=0.0,
                step=1.0,
                value=expense["amount"],
                key=f"amount_{record_key}",
                label_visibility="collapsed"
            )

        with col2:
            st.subheader("Category")
            updated_category = st.selectbox(
                label="Category",
                options=available_category,
                index=available_category.index(expense["category"]),
                key=f"category_{record_key}",
                label_visibility="collapsed"
            )

        with col3:
            st.subheader("Notes")
            updated_notes = st.text_input(
                label="Notes",
                value=expense["notes"],
                key=f"notes_{record_key}",
                label_visibility="collapsed"
            )

        with col4:
            st.write("")
            if st.button("Update", key=f"update_btn_{record_key}"):
                payload = {
                    "id":expense["id"],
                    "amount": updated_amount,
                    "category": updated_category,
                    "notes": updated_notes
                }

                update_response = requests.put(
                    f"{API_Url}/expenses/{expense['id']}",
                    json=payload
                )

                if update_response.status_code == 200:
                    st.success(f"Expense ID {expense['id']} updated successfully!")
                else:
                    st.error(f"Failed to update: {update_response.text}")
