import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 LinkedIn Analytics Dashboard")

# Upload file
file = st.file_uploader("Upload your LinkedIn Analytics CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Melt (convert wide → long format)
    df_long = df.melt(
        id_vars=["Sl. No.", "Channels", "Metrics"],
        var_name="Month",
        value_name="Value"
    )

    # Clean values (remove commas like 13,217)
    df_long["Value"] = df_long["Value"].astype(str).str.replace(",", "")
    df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")

    # Drop empty values
    df_long = df_long.dropna(subset=["Value"])

    st.subheader("📌 Cleaned Data")
    st.dataframe(df_long)

    # ---- KPI Selection ----
    st.subheader("📊 Select Metric")
    metric = st.selectbox("Choose a metric", df_long["Metrics"].unique())

    filtered = df_long[df_long["Metrics"] == metric]

    # ---- Monthly Trend ----
    st.subheader("📅 Monthly Trend")
    fig1 = px.line(filtered, x="Month", y="Value", markers=True, title=f"{metric} Trend")
    st.plotly_chart(fig1)

    # ---- KPI Total ----
    st.subheader("📈 Total Performance")
    total_value = int(filtered["Value"].sum())
    st.metric(label=f"Total {metric}", value=total_value)

    # ---- Quarterly Approximation ----
    # Group months manually into quarters
    def get_quarter(month):
        if "Jan" in month or "Feb" in month or "Mar" in month:
            return "Q1"
        elif "Apr" in month or "May" in month or "Jun" in month:
            return "Q2"
        elif "Jul" in month or "Aug" in month or "Sep" in month:
            return "Q3"
        elif "Oct" in month or "Nov" in month or "Dec" in month:
            return "Q4"
        else:
            return "Other"

    filtered["Quarter"] = filtered["Month"].apply(get_quarter)

    quarterly = filtered.groupby("Quarter")["Value"].sum().reset_index()

    st.subheader("📆 Quarterly Performance")
    fig2 = px.bar(quarterly, x="Quarter", y="Value", title=f"{metric} by Quarter")
    st.plotly_chart(fig2)

else:
    st.warning("Upload your file to generate dashboard")