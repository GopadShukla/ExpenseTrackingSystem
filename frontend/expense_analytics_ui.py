import streamlit as st
from datetime import  datetime
import requests
import pandas as pd
from dotenv import  load_dotenv
import  os
import altair as alt

load_dotenv()

API_Url=os.getenv("API_Url")

def expense_analytics():
    col1,col2= st.columns(2)
    with col1:
        start_date=st.date_input("Start Date", datetime.today())
    with col2:
        end_date = st.date_input("End Date", datetime.today())

    if st.button("Get Analytics"):
        payload={
            "start_date":start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response=requests.post(f"{API_Url}/analytics",json=payload)
        if response.status_code==200:
            response=response.json()
        else:
            st.error(f"Failed to get analytics: {response.status_code}")

        str_response={
            "Category":list(response.keys()),
            "Total": [value['total'] for key,value in response.items()],
            "Percentage": [value['percentage'] for key,value in response.items()]
        }

        df=pd.DataFrame(str_response)
        df_sorted=df.sort_values(by="Percentage",ascending=False)

        total_sum = df_sorted['Total'].astype(float).sum()

        col_sum, col_download = st.columns([3, 1.5])

        with col_sum:
            st.metric("💰 Total Expense", f"Rs. {total_sum:,.2f}")

        with col_download:
            csv = df_sorted.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Report as CSV",
                data=csv,
                file_name="expense_report.csv",
                mime="text/csv",
                use_container_width=True
            )

        chart = alt.Chart(df_sorted).mark_bar().encode(
            x=alt.X('Category:N', sort=None, axis=alt.Axis(labelAngle=0)),  # labelAngle=0 -> horizontal
            y='Percentage:Q'
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        st.dataframe(df_sorted.style.format({
            "Total": "Rs.{:,.2f}",
            "Percentage": "{:.2f} %"
        }), use_container_width=True)



