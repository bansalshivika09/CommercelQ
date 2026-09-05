import os

import streamlit as st
import pandas as pd
import plotly.express as px

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT + OPENAI
# =========================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    timeout=60.0
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Online Retail Intelligence",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("online_retail_final.csv")

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Revenue"] = pd.to_numeric(
        df["Revenue"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    df["Hour"] = pd.to_numeric(
        df["Hour"],
        errors="coerce"
    )

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Retail Intelligence")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Executive Overview",
        "🛍️ Product Intelligence",
        "👥 Customer Intelligence",
        "🌍 Geographic Analysis",
        "⏰ Time Analysis",
        "🤖 GenAI Business Analyst"
    ]
)


# =========================================================
# FILTERS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

countries = sorted(
    df["Country"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    countries
)


years = sorted(
    df["Year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "Year",
    years
)


transaction_types = sorted(
    df["Transaction_Type"].dropna().unique()
)

selected_transaction_types = st.sidebar.multiselect(
    "Transaction Type",
    transaction_types
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_countries:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_countries)
    ]


if selected_years:

    filtered_df = filtered_df[
        filtered_df["Year"].isin(selected_years)
    ]


if selected_transaction_types:

    filtered_df = filtered_df[
        filtered_df["Transaction_Type"].isin(
            selected_transaction_types
        )
    ]


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "🏠 Executive Overview":

    st.title("📊 Online Retail Intelligence")

    st.caption(
        "Executive overview of sales, customers, products and revenue trends."
    )

    st.divider()

    total_revenue = filtered_df["Revenue"].sum()
    total_units = filtered_df["Quantity"].sum()
    total_transactions = filtered_df["Invoice"].nunique()
    total_customers = filtered_df["Customer_ID"].nunique()

    if total_transactions > 0:
        aov = total_revenue / total_transactions
    else:
        aov = 0

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )

    col2.metric(
        "Total Units",
        f"{total_units:,.0f}"
    )

    col3.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col4.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col5.metric(
        "Average Order Value",
        f"${aov:,.2f}"
    )

    st.divider()

    # -----------------------------------------------------
    # MONTHLY REVENUE
    # -----------------------------------------------------

    monthly = (
        filtered_df
        .groupby(
            "Year_Month",
            as_index=False
        )["Revenue"]
        .sum()
        .sort_values("Year_Month")
    )

    fig_monthly = px.line(
        monthly,
        x="Year_Month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # TOP COUNTRIES
    # -----------------------------------------------------

    with col1:

        country_revenue = (
            filtered_df
            .groupby(
                "Country",
                as_index=False
            )["Revenue"]
            .sum()
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10)
        )

        fig_country = px.bar(
            country_revenue,
            x="Revenue",
            y="Country",
            orientation="h",
            title="Top 10 Countries by Revenue"
        )

        fig_country.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    # -----------------------------------------------------
    # TOP PRODUCTS
    # -----------------------------------------------------

    with col2:

        product_revenue = (
            filtered_df
            .groupby(
                "Description",
                as_index=False
            )["Revenue"]
            .sum()
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10)
        )

        fig_product = px.bar(
            product_revenue,
            x="Revenue",
            y="Description",
            orientation="h",
            title="Top 10 Products by Revenue"
        )

        fig_product.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            }
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )


# =========================================================
# PRODUCT INTELLIGENCE
# =========================================================

elif page == "🛍️ Product Intelligence":

    st.title("🛍️ Product Intelligence")

    st.caption(
        "Identify high-performing products and product-level opportunities."
    )

    st.divider()

    product_revenue = (
        filtered_df
        .groupby(
            "Description",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(20)
    )

    fig = px.bar(
        product_revenue.head(10),
        x="Revenue",
        y="Description",
        orientation="h",
        title="Top 10 Products by Revenue"
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Product Volume vs Revenue")

    product_analysis = (
        filtered_df
        .groupby(
            "Description",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Quantity=("Quantity", "sum")
        )
    )

    fig_scatter = px.scatter(
        product_analysis,
        x="Quantity",
        y="Revenue",
        hover_name="Description",
        title="Quantity vs Revenue"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    st.subheader("Product Performance")

    st.dataframe(
        product_revenue,
        use_container_width=True
    )


# =========================================================
# CUSTOMER INTELLIGENCE
# =========================================================

elif page == "👥 Customer Intelligence":

    st.title("👥 Customer Intelligence")

    st.caption(
        "Analyze customer value, transaction frequency and loyalty."
    )

    st.divider()

    customer_analysis = (
        filtered_df
        .dropna(subset=["Customer_ID"])
        .groupby(
            "Customer_ID",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Invoice", "nunique"),
            Units=("Quantity", "sum")
        )
    )

    customer_analysis["AOV"] = (
        customer_analysis["Revenue"] /
        customer_analysis["Transactions"]
    )

    top_customers = (
        customer_analysis
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig_customer = px.bar(
        top_customers,
        x="Customer_ID",
        y="Revenue",
        title="Top 10 Customers by Revenue"
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

    fig_scatter = px.scatter(
        customer_analysis,
        x="Transactions",
        y="Revenue",
        size="Units",
        hover_name="Customer_ID",
        title="Customer Transactions vs Revenue"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    customer_analysis["Customer_Type"] = (
        customer_analysis["Transactions"]
        .apply(
            lambda x:
            "Repeat Customer"
            if x > 1
            else "One-Time Customer"
        )
    )

    loyalty = (
        customer_analysis
        .groupby("Customer_Type")
        .size()
        .reset_index(name="Customers")
    )

    fig_loyalty = px.pie(
        loyalty,
        names="Customer_Type",
        values="Customers",
        title="Repeat vs One-Time Customers"
    )

    st.plotly_chart(
        fig_loyalty,
        use_container_width=True
    )


# =========================================================
# GEOGRAPHIC ANALYSIS
# =========================================================

elif page == "🌍 Geographic Analysis":

    st.title("🌍 Geographic Analysis")

    st.caption(
        "Understand revenue concentration and customer activity across countries."
    )

    st.divider()

    country_analysis = (
        filtered_df
        .groupby(
            "Country",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Invoice", "nunique"),
            Customers=("Customer_ID", "nunique")
        )
    )

    country_analysis["AOV"] = (
        country_analysis["Revenue"] /
        country_analysis["Transactions"]
    )

    top_countries = (
        country_analysis
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(15)
    )

    fig_country = px.bar(
        top_countries,
        x="Revenue",
        y="Country",
        orientation="h",
        title="Top Countries by Revenue"
    )

    fig_country.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

    st.subheader("Country Performance")

    st.dataframe(
        country_analysis.sort_values(
            "Revenue",
            ascending=False
        ),
        use_container_width=True
    )


# =========================================================
# TIME ANALYSIS
# =========================================================

elif page == "⏰ Time Analysis":

    st.title("⏰ Time & Sales Analysis")

    st.caption(
        "Identify when customers purchase and when revenue is generated."
    )

    st.divider()

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_revenue = (
        filtered_df
        .groupby(
            "Day_Of_Week",
            as_index=False
        )["Revenue"]
        .sum()
    )

    day_revenue["Day_Of_Week"] = pd.Categorical(
        day_revenue["Day_Of_Week"],
        categories=day_order,
        ordered=True
    )

    day_revenue = day_revenue.sort_values(
        "Day_Of_Week"
    )

    fig_day = px.bar(
        day_revenue,
        x="Day_Of_Week",
        y="Revenue",
        title="Revenue by Day of Week"
    )

    st.plotly_chart(
        fig_day,
        use_container_width=True
    )

    hour_revenue = (
        filtered_df
        .groupby(
            "Hour",
            as_index=False
        )["Revenue"]
        .sum()
        .sort_values("Hour")
    )

    fig_hour = px.line(
        hour_revenue,
        x="Hour",
        y="Revenue",
        markers=True,
        title="Revenue by Hour"
    )

    fig_hour.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


# =========================================================
# GENAI BUSINESS ANALYST
# =========================================================

elif page == "🤖 GenAI Business Analyst":

    st.title("🤖 GenAI Business Analyst")

    st.caption(
        "Ask business questions and generate evidence-based insights "
        "from the retail dataset."
    )

    st.divider()

    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    question = st.selectbox(
        "Choose a business question",

        [
            "Explain the overall revenue performance",
            "Analyze product performance",
            "Analyze customer behavior",
            "Analyze country performance",
            "Analyze purchasing trends",
            "Give overall business recommendations"
        ]
    )

    # -----------------------------------------------------
    # CALCULATE METRICS
    # -----------------------------------------------------

    total_revenue = filtered_df["Revenue"].sum()

    total_units = filtered_df["Quantity"].sum()

    total_transactions = filtered_df["Invoice"].nunique()

    total_customers = filtered_df["Customer_ID"].nunique()

    if total_transactions > 0:

        aov = (
            total_revenue /
            total_transactions
        )

    else:

        aov = 0

    # -----------------------------------------------------
    # TOP COUNTRY
    # -----------------------------------------------------

    country_revenue = (
        filtered_df
        .groupby("Country")["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(country_revenue) > 0:

        top_country = country_revenue.index[0]

        top_country_revenue = country_revenue.iloc[0]

    else:

        top_country = "N/A"

        top_country_revenue = 0

    # -----------------------------------------------------
    # TOP PRODUCT
    # -----------------------------------------------------

    product_revenue = (
        filtered_df
        .groupby("Description")["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(product_revenue) > 0:

        top_product = product_revenue.index[0]

        top_product_revenue = product_revenue.iloc[0]

    else:

        top_product = "N/A"

        top_product_revenue = 0

    # -----------------------------------------------------
    # TOP CUSTOMER
    # -----------------------------------------------------

    customer_revenue = (
        filtered_df
        .dropna(subset=["Customer_ID"])
        .groupby("Customer_ID")["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(customer_revenue) > 0:

        top_customer = customer_revenue.index[0]

        top_customer_revenue = customer_revenue.iloc[0]

    else:

        top_customer = "N/A"

        top_customer_revenue = 0

    # -----------------------------------------------------
    # PEAK HOUR
    # -----------------------------------------------------

    hourly_revenue = (
        filtered_df
        .groupby("Hour")["Revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    if len(hourly_revenue) > 0:

        peak_hour = hourly_revenue.index[0]

        peak_hour_revenue = hourly_revenue.iloc[0]

    else:

        peak_hour = "N/A"

        peak_hour_revenue = 0

    # -----------------------------------------------------
    # REPEAT CUSTOMERS
    # -----------------------------------------------------

    customer_transactions = (
        filtered_df
        .dropna(subset=["Customer_ID"])
        .groupby("Customer_ID")["Invoice"]
        .nunique()
    )

    repeat_customers = (
        customer_transactions > 1
    ).sum()

    one_time_customers = (
        customer_transactions == 1
    ).sum()

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

    col2.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col3.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "AOV",
        f"${aov:,.2f}"
    )

    st.divider()

    # -----------------------------------------------------
    # DATA SUMMARY
    # -----------------------------------------------------

    st.subheader("📊 Data Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Top Country:** {top_country}"
        )

        st.write(
            f"**Top Country Revenue:** "
            f"${top_country_revenue:,.2f}"
        )

        st.write(
            f"**Top Product:** {top_product}"
        )

        st.write(
            f"**Top Product Revenue:** "
            f"${top_product_revenue:,.2f}"
        )

    with col2:

        st.write(
            f"**Top Customer:** {top_customer}"
        )

        st.write(
            f"**Top Customer Revenue:** "
            f"${top_customer_revenue:,.2f}"
        )

        if peak_hour != "N/A":

            st.write(
                f"**Peak Purchasing Hour:** {peak_hour}:00"
            )

        else:

            st.write(
                "**Peak Purchasing Hour:** N/A"
            )

        st.write(
            f"**Repeat Customers:** "
            f"{repeat_customers:,}"
        )

        st.write(
            f"**One-Time Customers:** "
            f"{one_time_customers:,}"
        )

    st.divider()

    # -----------------------------------------------------
    # GENERATE AI INSIGHT
    # -----------------------------------------------------

    if st.button(
        "🤖 Generate AI Insight",
        use_container_width=True
    ):

        business_data = f"""
Retail Business Metrics

Total Revenue:
${total_revenue:,.2f}

Total Units Sold:
{total_units:,.0f}

Total Transactions:
{total_transactions:,}

Total Customers:
{total_customers:,}

Average Order Value:
${aov:,.2f}

Top Country:
{top_country}

Top Country Revenue:
${top_country_revenue:,.2f}

Top Product:
{top_product}

Top Product Revenue:
${top_product_revenue:,.2f}

Top Customer:
{top_customer}

Top Customer Revenue:
${top_customer_revenue:,.2f}

Peak Purchasing Hour:
{peak_hour}:00

Peak Hour Revenue:
${peak_hour_revenue:,.2f}

Repeat Customers:
{repeat_customers:,}

One-Time Customers:
{one_time_customers:,}
"""

        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are a professional retail business analyst.

Analyze the following actual retail business data:

{business_data}

The user wants to know:

{question}

Provide the answer using exactly these sections:

### 💡 Key Insight

Explain the most important finding from the data.

### 🔍 Analysis

Explain what the data suggests and possible business reasons.

### 🎯 Business Recommendation

Give 2-3 practical recommendations based only on the available data.

Important rules:

- Use only the data provided.
- Do not invent statistics.
- Do not make up numbers.
- Do not claim information that is not supported by the data.
- Clearly distinguish observations from possible explanations.
- Keep the response concise.
- Focus on actionable business insights.
"""

        # -------------------------------------------------
        # AI REQUEST
        # -------------------------------------------------

        try:

            with st.spinner(
                "🤖 Analyzing your retail data..."
            ):

                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt,
                    timeout=60.0
                )

            st.success(
                "AI business analysis generated!"
            )

            st.markdown(
                response.output_text
            )

        except Exception as e:

            st.error(
                f"Unable to generate AI insight: "
                f"{type(e).__name__}: {e}"
            )