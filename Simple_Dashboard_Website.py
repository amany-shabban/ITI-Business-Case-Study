import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

#  Page content
st.set_page_config(page_title="ITI KPI Dashboard", layout="wide")

# Load the dataset
ITI_data = pd.read_csv("ITI_DATASet.csv")

# Track filter
tracks = sorted(ITI_data["track"].dropna().unique())
selected_track = st.sidebar.selectbox("Choose Track : ", ["All Tracks"] + list(tracks))

if selected_track != "All Tracks":
    df = ITI_data[ITI_data["track"] == selected_track]
else:
    df = ITI_data

# Prepare dashboard KPIs
graduation_rate = df["graduated_flag"].mean() * 100
Avg_Attendance = df["attendance_rate"].mean() * 100
Avg_Exam = df["exams_score"].mean()
Freelancers = (df["employment_status"] == "Freelancer").mean() * 100

employment = ['Intern', 'Freelancer', 'Part-time', 'Full-time']
employment_rate = df["employment_status"].isin(employment).mean() * 100

freelance_income_rate = (
    df[df["employment_status"] == "Freelancer"]
    .groupby("track")["freelancing_income_usd_total"]
    .mean()
)

# ===== Styling & KPI Cards =====
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

st.title("ITI Students KPI Dashboard")

# ===== KPIs Section =====
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Graduation Rate</div>
            <div class="kpi-value">{graduation_rate:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Employment Rate</div>
            <div class="kpi-value">{employment_rate:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Freelancers %</div>
            <div class="kpi-value">{Freelancers:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

col4, col5 = st.columns(2)
with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Exam Score</div>
            <div class="kpi-value">{Avg_Exam:.1f}</div>
        </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Attendance</div>
            <div class="kpi-value">{Avg_Attendance:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

# ===== Bar chart: Freelance Income =====
st.subheader("Average Freelance Income by Track")
st.bar_chart(freelance_income_rate, color="#00CDAC", height=400)

# ================================
# Additional Visualizations Section
# ================================
st.markdown("---")
st.header("Detailed Analysis & Visuals") 

COLOR_PALETTE = ['#00CDAC', '#151B54', '#74737A', '#4A90E2', '#E94B3C', '#F39C12', '#9B59B6', '#1ABC9C']

# -----------------------------
# Distribution of Exam Scores
# -----------------------------
st.subheader("Exam Score Distribution")
fig_exam = px.histogram(
    ITI_data,
    x="exams_score",
    nbins=20,
    color_discrete_sequence=["#00CDAC"],
    title="Distribution of Exam Scores among Students"
)
fig_exam.update_layout(
    plot_bgcolor="white",
    title_font_size=20,
    title_font_color="#F5F1F1",
    height=500,
    xaxis=dict(
        title="Exam Score",
        titlefont=dict(size=18, color="#F5F1F1"),
        tickfont=dict(size=16, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        title="Number of Students",
        titlefont=dict(size=18, color="#F5F1F1"),
        tickfont=dict(size=16, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    )
)
st.plotly_chart(fig_exam, use_container_width=True)

# -----------------------------
# Attendance vs Exam Scatter
# -----------------------------
st.subheader("Attendance vs Exam Score")
fig_scatter = px.scatter(
    ITI_data,
    x="attendance_rate",
    y="exams_score",
    color="track",
    title="Attendance vs Exam Score by Track",
    color_discrete_sequence=COLOR_PALETTE
)
fig_scatter.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color='white')))
fig_scatter.update_layout(
    plot_bgcolor="white",
    title_font_size=20,
    title_font_color="#F5F1F1",
    height=550,
    xaxis=dict(
        title="Attendance Rate (%)",
        titlefont=dict(size=18, color="#F5F1F1"),
        tickfont=dict(size=16, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        title="Exam Score",
        titlefont=dict(size=18, color="#F5F1F1"),
        tickfont=dict(size=16, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    ),
    legend=dict(
        font=dict(size=14, color="#F5F1F1"),
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#F5F1F1",
        borderwidth=1
    )
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Employment Status by Track (Altair) - 
# -----------------------------
st.subheader("Employment Status Distribution by Track")
employment_chart = (
    alt.Chart(ITI_data)
    .mark_bar()
    .encode(
        x=alt.X("track:N", title="Track", axis=alt.Axis(labelFontSize=16, titleFontSize=18, labelColor="#F5F1F1", titleColor="#F5F1F1")),
        y=alt.Y("count()", title="Number of Students", axis=alt.Axis(labelFontSize=16, titleFontSize=18, labelColor="#F5F1F1", titleColor="#F5F1F1")),
        color=alt.Color("employment_status:N", title="Employment Status", scale=alt.Scale(range=COLOR_PALETTE)),
        tooltip=["track", "employment_status", "count()"]
    )
    .properties(width="container", height=500)
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridColor='#E0E0E0')
    .configure_legend(labelFontSize=16, titleFontSize=18, labelColor="#F5F1F1", titleColor="#F5F1F1")
)
st.altair_chart(employment_chart, use_container_width=True)

# -----------------------------
# Freelance Income by Track (Plotly)
# -----------------------------
st.subheader("Average Freelance Income per Track")
freelance_income_df = ITI_data[ITI_data["employment_status"] == "Freelancer"].groupby("track")["freelancing_income_usd_total"].mean().reset_index()
fig_income = px.bar(
    freelance_income_df,
    x="track",
    y="freelancing_income_usd_total",
    text_auto=".2f",
    color="track",
    color_discrete_sequence=COLOR_PALETTE,
    title="Average Freelance Income by Track"
)
fig_income.update_layout(
    plot_bgcolor="white",
    title_font_size=20,
    title_font_color="#F5F1F1",
    height=550,
    showlegend=False,
    xaxis=dict(
        title="Track",
        titlefont=dict(size=16, color="#F5F1F1"),
        tickfont=dict(size=14, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        title="Average Freelance Income (USD)",
        titlefont=dict(size=18, color="#F5F1F1"),
        tickfont=dict(size=16, color="#F5F1F1"),
        gridcolor='#E0E0E0'
    )
)
fig_income.update_traces(textfont=dict(size=16, color='white'), textposition='outside')
st.plotly_chart(fig_income, use_container_width=True)

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("Correlation Between Numeric Features")
numeric_cols = ITI_data.select_dtypes(include='number')
corr = numeric_cols.corr()
fig_corr = px.imshow(
    corr,
    text_auto='.2f',
    color_continuous_scale="Tealgrn",
    title="Correlation Heatmap",
    aspect="auto"
)
fig_corr.update_layout(
    title_font_size=20,
    title_font_color="#F5F1F1",
    height=600,
    xaxis=dict(
        tickfont=dict(size=12, color="#F5F1F1")
    ),
    yaxis=dict(
        tickfont=dict(size=12, color="#F5F1F1")
    )
)
fig_corr.update_traces(textfont=dict(size=11))
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")
st.caption("Dashboard created using Streamlit | Plotly | Altair")