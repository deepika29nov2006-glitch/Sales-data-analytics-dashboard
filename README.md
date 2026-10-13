# Sales Data Analytics Dashboard

## Project Overview
The Sales Data Analytics Dashboard is a Python-based web application that helps users analyze sales data through interactive charts, key performance indicators (KPIs), and data filters.

The dashboard is developed using Python, Pandas, Streamlit, and Plotly.

## Features
- Displays total revenue, total orders, units sold, and average revenue per order.
- Shows monthly sales revenue using an interactive line chart.
- Displays category-wise and region-wise revenue.
- Allows users to add new sales orders through a form.
- Allows users to upload sales data using a CSV file.
- Supports adding uploaded records to existing data or replacing existing data.
- Provides category and region filters.
- Displays sales transaction records in a table.
- Allows users to download filtered sales data as a CSV file.

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly
- CSV

## Dataset Description
The dataset contains the following columns:

| Column | Description |
|---|---|
| OrderID | Unique order identification number |
| OrderDate | Date of the order |
| Product | Name of the product |
| Category | Product category |
| Quantity | Number of units sold |
| UnitPrice | Price per unit |
| Region | Sales region |

The dashboard calculates revenue using:

**Revenue = Quantity × Unit Price**

The project uses sample sales data for demonstration. It does not represent actual company sales.

## Project Structure

```text
Sales_Data_Analytics_Mini_Project/
│
├── app.py
├── sales_data.csv
├── requirements.txt
└── README.md
```

## Installation and Setup

### Step 1: Install Python
Install Python on your computer if it is not already installed.

### Step 2: Open the Project
Open the project folder in Visual Studio Code.

### Step 3: Install Required Libraries
Open the VS Code terminal and run:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard
Run this command in the terminal:

```bash
python -m streamlit run app.py
```

If `python` does not work on Windows, try:

```bash
py -m streamlit run app.py
```

### Step 5: Open the Application
Streamlit will provide a local URL, usually:

`http://localhost:8501`

Open the URL in your browser to use the dashboard.

## How to Use the Dashboard
1. View the sales KPIs at the top of the dashboard.
2. Apply category and region filters.
3. Explore the monthly, category-wise, and region-wise charts.
4. Add a new sales order using the order form.
5. Upload a CSV file containing sales records.
6. Download the filtered sales data when required.

## Key Benefits
- Makes sales data easier to understand.
- Helps identify high-performing product categories and regions.
- Supports basic sales monitoring and analysis.
- Provides interactive data visualization.
- Allows users to add and upload sales records.

## Limitations
- The project uses sample data for demonstration.
- Sales orders added through the application are saved to the local CSV file.
- Persistent storage may not be guaranteed when the application is deployed on a cloud platform.
- The dashboard calculates revenue, not profit.

## Future Scope
- Connect the dashboard to a database.
- Add sales forecasting using machine learning.
- Include profit and profit-margin analysis.
- Add user authentication and role-based access.
- Improve data storage for cloud deployment.

## Conclusion
The Sales Data Analytics Dashboard demonstrates how Python and data visualization tools can be used to analyze sales information through an interactive web application. It provides useful sales summaries, charts, filtering, CSV upload, and data export features.

## Author
Developed as a mini project for learning Python-based data analytics and interactive dashboard development.