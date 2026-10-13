from pathlib import Path
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sales Data Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

DATA_FILE = Path(__file__).parent / "sales_data.csv"

COLUMNS = [
    "OrderID", "OrderDate", "Product",
    "Category", "Quantity", "UnitPrice", "Region"
]

CATEGORIES = [
    "Electronics", "Clothing", "Beauty", "Home", "Other"
]

REGIONS = [
    "North", "South", "East", "West", "Central", "Other"
]


# Read and clean sales data
def clean_data(data):
    data = data.copy()
    data.columns = [str(c).strip() for c in data.columns]

    missing = [c for c in COLUMNS if c not in data.columns]
    if missing:
        raise ValueError(
            "CSV is missing columns: " + ", ".join(missing)
        )

    data = data[COLUMNS].copy()

    data["OrderID"] = pd.to_numeric(
        data["OrderID"], errors="coerce"
    )
    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"], errors="coerce"
    )
    data["Quantity"] = pd.to_numeric(
        data["Quantity"], errors="coerce"
    )
    data["UnitPrice"] = pd.to_numeric(
        data["UnitPrice"], errors="coerce"
    )

    for column in ["Product", "Category", "Region"]:
        data[column] = data[column].astype("string").str.strip()

    data = data.dropna(subset=COLUMNS)

    data = data[
        (data["OrderID"] > 0)
        & (data["Quantity"] > 0)
        & (data["UnitPrice"] >= 0)
        & (data["Product"] != "")
        & (data["Category"] != "")
        & (data["Region"] != "")
    ].copy()

    if data["OrderID"].duplicated().any():
        raise ValueError("Order IDs must be unique.")

    data["OrderID"] = data["OrderID"].astype(int)
    data["Quantity"] = data["Quantity"].astype(int)
    data["Revenue"] = data["Quantity"] * data["UnitPrice"]
    data["Month"] = data["OrderDate"].dt.to_period("M").astype(str)

    return data.sort_values(
        ["OrderDate", "OrderID"]
    ).reset_index(drop=True)


# Save data to CSV
def save_data(data):
    output = data[COLUMNS].copy()
    output["OrderDate"] = pd.to_datetime(
        output["OrderDate"]
    ).dt.strftime("%Y-%m-%d")

    output.to_csv(DATA_FILE, index=False)


st.title("📊 Sales Data Analytics Dashboard")
st.write(
    "Add sales orders, upload CSV files, "
    "and explore updated sales charts."
)

# Check whether the CSV exists
if not DATA_FILE.exists():
    st.error(
        "sales_data.csv was not found. "
        "Keep it in the same folder as app.py."
    )
    st.stop()

try:
    base_data = clean_data(pd.read_csv(DATA_FILE))
except Exception as error:
    st.error(f"Could not read sales data: {error}")
    st.stop()


# Add a new sales order
with st.expander("➕ Add a New Sales Order"):
    next_id = (
        int(base_data["OrderID"].max()) + 1
        if not base_data.empty else 1001
    )

    with st.form("add_order_form"):
        order_id = st.number_input(
            "Order ID", min_value=1, value=next_id, step=1
        )

        order_date = st.date_input(
            "Order Date", value=date.today()
        )

        product = st.text_input(
            "Product Name", placeholder="Wireless Mouse"
        )

        category = st.selectbox("Category", CATEGORIES)

        quantity = st.number_input(
            "Quantity", min_value=1, value=1, step=1
        )

        price = st.number_input(
            "Price per Item (₹)", min_value=0.0,
            value=500.0, step=50.0
        )

        region = st.selectbox("Region", REGIONS)

        st.write(f"Order Revenue: ₹{quantity * price:,.2f}")

        save_order = st.form_submit_button(
            "Save Order", type="primary"
        )

    if save_order:
        if not product.strip():
            st.error("Please enter a product name.")

        elif int(order_id) in set(base_data["OrderID"]):
            st.error("This Order ID already exists.")

        else:
            new_order = pd.DataFrame([{
                "OrderID": int(order_id),
                "OrderDate": pd.Timestamp(order_date),
                "Product": product.strip(),
                "Category": category,
                "Quantity": int(quantity),
                "UnitPrice": float(price),
                "Region": region
            }])

            combined = pd.concat(
                [base_data[COLUMNS], new_order],
                ignore_index=True
            )

            try:
                clean_data(combined)
                save_data(combined)
                st.success("New order saved successfully!")
                st.rerun()
            except Exception as error:
                st.error(f"Could not save order: {error}")


# Upload a CSV file
with st.expander("📤 Upload Sales CSV"):
    st.write("Required columns:")
    st.code(", ".join(COLUMNS))

    uploaded_file = st.file_uploader(
        "Choose a CSV file", type=["csv"]
    )

    upload_mode = st.radio(
        "Import option",
        ["Add to existing data", "Replace existing data"]
    )

    if st.button("Import CSV", disabled=uploaded_file is None):
        try:
            uploaded_data = clean_data(
                pd.read_csv(uploaded_file)
            )

            if uploaded_data.empty:
                st.error("The uploaded file has no valid rows.")

            elif upload_mode == "Add to existing data":
                combined = pd.concat(
                    [base_data[COLUMNS],
                     uploaded_data[COLUMNS]],
                    ignore_index=True
                )

                if combined["OrderID"].duplicated().any():
                    st.error(
                        "Duplicate Order IDs found. "
                        "Please make the IDs unique."
                    )
                else:
                    save_data(combined)
                    st.success("CSV data added successfully!")
                    st.rerun()

            else:
                save_data(uploaded_data)
                st.success("Sales data replaced successfully!")
                st.rerun()

        except Exception as error:
            st.error(
                f"CSV import failed. Check the column names "
                f"and data. Details: {error}"
            )


# Reload the latest saved data
try:
    data = clean_data(pd.read_csv(DATA_FILE))
except Exception as error:
    st.error(f"Could not reload data: {error}")
    st.stop()


# Dashboard filters
with st.sidebar:
    st.header("Dashboard Filters")

    categories = sorted(data["Category"].unique().tolist())
    regions = sorted(data["Region"].unique().tolist())

    selected_categories = st.multiselect(
        "Select Categories",
        categories,
        default=categories
    )

    selected_regions = st.multiselect(
        "Select Regions",
        regions,
        default=regions
    )


filtered = data[
    data["Category"].isin(selected_categories)
    & data["Region"].isin(selected_regions)
].copy()

if filtered.empty:
    st.warning(
        "No data matches these filters. "
        "Select categories and regions in the sidebar."
    )
    st.stop()


# Calculate dashboard metrics
revenue = filtered["Revenue"].sum()
orders = filtered["OrderID"].nunique()
units = filtered["Quantity"].sum()
average_order = revenue / orders if orders else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{revenue:,.2f}")
col2.metric("Total Orders", f"{orders:,}")
col3.metric("Units Sold", f"{units:,}")
col4.metric("Average Revenue / Order", f"₹{average_order:,.2f}")


# Monthly revenue chart
monthly = (
    filtered.groupby("Month", as_index=False)["Revenue"]
    .sum()
    .sort_values("Month")
)

# Category revenue chart
by_category = (
    filtered.groupby("Category", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
)

# Region revenue chart
by_region = (
    filtered.groupby("Region", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
)


left, right = st.columns(2)

with left:
    st.subheader("Monthly Revenue Trend")
    fig = px.line(
        monthly, x="Month", y="Revenue",
        markers=True, title="Revenue by Month"
    )
    fig.update_layout(yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Revenue by Category")
    fig = px.bar(
        by_category, x="Category", y="Revenue",
        color="Category", title="Category Sales"
    )
    fig.update_layout(
        yaxis_title="Revenue (₹)", showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


left, right = st.columns(2)

with left:
    st.subheader("Revenue by Region")
    fig = px.bar(
        by_region, x="Region", y="Revenue",
        color="Region", title="Regional Sales"
    )
    fig.update_layout(
        yaxis_title="Revenue (₹)", showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Quick Insights")

    if not by_category.empty:
        st.write(
            "**Top Category:**",
            by_category.iloc[0]["Category"]
        )

    if not by_region.empty:
        st.write(
            "**Top Region:**",
            by_region.iloc[0]["Region"]
        )

    if not monthly.empty:
        top_month = monthly.loc[
            monthly["Revenue"].idxmax(), "Month"
        ]
        st.write("**Best Sales Month:**", top_month)

    st.info(
        "Revenue = Quantity × Unit Price. "
        "Revenue is not the same as profit."
    )


# Display transactions and download CSV
st.subheader("Sales Transactions")

display_data = filtered[
    ["OrderID", "OrderDate", "Product", "Category",
     "Quantity", "UnitPrice", "Revenue", "Region"]
].copy()

display_data["OrderDate"] = (
    display_data["OrderDate"].dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_data, use_container_width=True, hide_index=True
)

st.download_button(
    "⬇️ Download Filtered Sales CSV",
    data=display_data.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.caption(
    "The starter dataset contains synthetic sample data "
    "for demonstration, not real company transactions."
)