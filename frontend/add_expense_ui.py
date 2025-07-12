import streamlit as st
from datetime import  datetime
import requests
from dotenv import  load_dotenv
import  os

load_dotenv()

API_Url=os.getenv("API_Url")


def add_expense_tab():
    st.header("➕ Add New Expenses")
    selected_date = st.date_input("Enter Date", datetime.today())

    existing_expense = []
    available_category = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="add_expense_form"):
        expenses = []
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")
        for i in range(5):

            if i < len(existing_expense):
                amount = existing_expense[i]["amount"]
                category = existing_expense[i]["category"]
                notes = existing_expense[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            with col1:
                expense_amount = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                                 label_visibility="collapsed")

            with col2:
                expense_category = st.selectbox(label="Category", options=available_category,
                                                index=available_category.index(category), key=f"category_{i}",
                                                label_visibility="collapsed")

            with col3:
                expense_notes = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                "amount": expense_amount,
                "category": expense_category,
                "notes": expense_notes
            })
        submit_button = st.form_submit_button("Add Expenses")
        if submit_button:
            filtered_expense = [expense for expense in expenses if expense['amount'] > 0]
            if not filtered_expense:
                st.warning("Please enter at least one valid expense amount greater than 0.")
                return

            with st.spinner("💾 Saving expenses..."):
                response = requests.post(
                    f"{API_Url}/expenses/{selected_date}",
                    json=filtered_expense
                )
                if response.status_code == 200:
                    st.success("✅ New expenses added successfully!")
                else:
                    st.error(f"❌ Failed to add expenses: {response.text}")