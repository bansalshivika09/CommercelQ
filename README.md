# CommercelQ
🛍️ Online Retail Intelligence & Analytics

📌 Project Overview

 Developed an **end-to-end retail analytics project** using a large online retail transaction dataset containing **500K+ records**. The objective was to transform raw transactional data into **meaningful business insights and actionable recommendations**.
Built the project using the workflow: **Data Cleaning → EDA → SQL Analysis → Interactive Dashboard → GenAI Insights**.

 🧹 Data Cleaning & Preparation

 Loaded and processed the retail dataset using **Python and Pandas**.
Cleaned transactional data and handled missing customer information.
Converted `InvoiceDate` into a proper datetime format.
Created additional analytical features such as:

Year
Month
Month Name
Year-Month
Day of Week
Hour
Created a **Revenue** metric using transaction quantity and price.
Classified transactions based on transaction type for further customer and sales analysis.

 📊 Exploratory Data Analysis

Performed EDA to understand overall sales and customer behavior.
Analyzed:

Total Revenue
Total Units Sold
Total Transactions
Total Customers
Average Order Value (AOV)
Identified top-performing products and countries**.
Analyzed revenue trends across months, days, and purchasing hours.
Investigated customer purchasing behavior and transaction patterns.

🗄️ SQL Business Analysis

I use Python to answer practical business questions, including:

* Which countries generate the highest revenue?
* Which products generate the highest revenue?
* Who are the top customers by revenue?
* What is the distribution of **repeat vs one-time customers**?
* How does revenue change month by month?
* Which days generate the most revenue?
* What are the **peak purchasing hours**?
* Which countries have the highest **Average Order Value**?
* Which products have **high sales volume but relatively low revenue**?
* Which frequent customers have a **low AOV**?

 📈 Streamlit Dashboard

Developed an interactive Streamlit dashboard** for business users.
Added multiple analytical sections:

  * 🏠 **Executive Overview**
  * 🛍️ **Product Intelligence**
  * 👥 **Customer Intelligence**
  * 🌍 **Geographic Analysis**
  * ⏰ **Time Analysis**
  * 🤖 **GenAI Business Analyst**
* Added interactive filters for:

  * Country
  * Year
  * Transaction Type
* Created KPI cards, tables, charts, and interactive visualizations.
* Used **Plotly** to visualize revenue, customer, product, geographic, and time-based trends.

### 🤖 Generative AI Integration

* Integrated the **OpenAI API** into the Streamlit application.
* Developed a **GenAI Business Analyst** that interprets actual analytical results.
* Users can ask questions such as:

  * Explain overall revenue performance
  * Analyze product performance
  * Analyze customer behavior
  * Analyze country performance
  * Analyze purchasing trends
  * Provide overall business recommendations
* Designed prompts to ensure the AI:

  * Uses only the provided analytical data
  * Does not invent statistics
  * Explains the business impact
  * Provides actionable recommendations
* AI responses are structured into:

  * **Key Insight**
  * **Analysis**
  * **Business Recommendation**

 🛠️ Tools & Technologies

| Tool / Technology    | Usage                                      |
| -------------------- | ------------------------------------------ |
| **Python**           | Data processing and analysis               |
| **Pandas**           | Data cleaning, transformation, aggregation |
| **NumPy**            | Numerical operations                       |
| **MySQL**            | Database storage and SQL business analysis |
| **SQL**              | Business queries and KPI analysis          |
| **Streamlit**        | Interactive web dashboard                  |
| **Plotly**           | Interactive data visualizations            |
| **OpenAI API**       | GenAI-powered business insights            |
| **Jupyter Notebook** | EDA and SQL analysis                       |
| **Git**              | Version control                            |
| **GitHub**           | Project repository and portfolio           |

💡 Business Value

* Helps identify **high-value customers, products, and markets**.
* Enables businesses to understand **when and where customers purchase**.
* Highlights potential opportunities to improve **revenue and AOV**.
* Combines traditional analytics with **Generative AI** to convert data into understandable business recommendations.
* Demonstrates an end-to-end **Data Analyst / Business Intelligence workflow** using real-world transactional data.
