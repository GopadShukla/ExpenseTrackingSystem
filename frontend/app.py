import streamlit as st
from add_expense_ui  import  add_expense_tab
from update_expense_ui import update_expense_tab
from expense_analytics_ui import  expense_analytics


st.title("Expense Tracking System")

tab1,tab2,tab3= st.tabs(["Add Expense","Update Expense","Expense Analytics"])

with tab1:
    add_expense_tab()

with tab2:
    update_expense_tab()

with tab3:
    expense_analytics()




