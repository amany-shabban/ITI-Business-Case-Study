import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
ITI_data = pd.read_csv("ITI_DATASet.csv")

# prepare dashboard  kpi cards
graduation_rate = ITI_data["graduated_flag"].mean()*100  
Avg_Attendance = ITI_data["attendance_rate"].mean()*100  

Avg_Exam = ITI_data["exams_score"].mean()
Freelancers = (ITI_data["employment_status"] == "Freelancer").mean()*100

employment = ['Intern','Freelancer','Part-time','Full-time']
employment_rate = ITI_data["employment_status"].isin(employment).mean()*100

freelance_income_rate = ITI_data[ITI_data["employment_status"] == "Freelancer"].groupby("track")["freelancing_income_usd_total"].mean()


# Build Dashboard
# st.columns(n)   divide webpage to N columns
# .metric()      used todisplay value as card
# st.markdown to make style cards

st.markdown("""
    <style>
    .kpi-card {
        background-color: #74737A;      
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #151B54;          
        margin-bottom: 15px;
    }
    .kpi-title {
        background-color: #151B54,  
        font-weight: bold;
        font-size: 19px;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #00CDAC;                  
    }
    </style>
""", unsafe_allow_html=True)

st.title("ITI Sudents KPI")
col1, col2, col3 = st.columns(3)

with col1:
      st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Graduation Rate</div>
            <div class="kpi-value">{graduation_rate:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class ="kpi-card">
                        <div class="kpi-title"> Employment Rate </div>
                        <div class="kpi-value">{employment_rate:.1f}%</div>
                  </div>"""
               ,unsafe_allow_html=True)

with col3:      
        st.markdown(f"""<div class ="kpi-card">
                        <div class="kpi-title">Freelancers %</div>
                        <div class="kpi-value">{Freelancers:.1f}%</div>
                  </div>"""

               ,unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
            st.markdown(f"""<div class ="kpi-card">
                        <div class="kpi-title">Average Exam Rate</div>
                        <div class="kpi-value">{Avg_Exam:.1f}%</div>
                  </div>"""

               ,unsafe_allow_html=True)
   
with col5:
    st.markdown(f"""<div class ="kpi-card">
                        <div class="kpi-title">Average Attandance</div>
                        <div class="kpi-value">{Avg_Attendance:.1f}%</div>
                    </div>"""

               ,unsafe_allow_html=True)

st.subheader("\nAverage Freelance Income by Track")

st.bar_chart(freelance_income_rate, color = "#00CDAC")
