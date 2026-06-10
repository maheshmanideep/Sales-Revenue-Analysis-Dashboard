import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales & Revenue Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("Analyze sales performance, revenue trends, and top-performing products.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)


if uploaded_file:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Convert Date Column
    df["Date"] = pd.to_datetime(df["Date"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    product = st.sidebar.multiselect(
        "Select Product",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Region"].isin(region)) &
        (df["Product"].isin(product))
    ]

    # KPI Calculations
    total_sales = filtered_df["Sales"].sum()
    total_revenue = filtered_df["Revenue"].sum()
    total_orders = filtered_df.shape[0]

    top_product = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    col3.metric("Total Orders", total_orders)
    col4.metric("Top Product", top_product)

    st.markdown("---")

    # Sales Trend
    sales_trend = filtered_df.groupby("Date")["Sales"].sum().reset_index()

    fig1 = px.line(
        sales_trend,
        x="Date",
        y="Sales",
        title="Sales Trend Over Time",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Revenue Trend
    revenue_trend = filtered_df.groupby("Date")["Revenue"].sum().reset_index()

    fig2 = px.area(
        revenue_trend,
        x="Date",
        y="Revenue",
        title="Revenue Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Top Products
    top_products = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )

    fig3 = px.bar(
        top_products,
        x="Product",
        y="Revenue",
        title="Top Performing Products",
        text_auto=True
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Region-wise Sales
    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales by Region",
        hole=0.4
    )

    st.plotly_chart(fig4, use_container_width=True)

    # Data Table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to view the dashboard.")