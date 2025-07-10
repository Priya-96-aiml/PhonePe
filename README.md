📊 Project Name: PhonePe Transaction Insights Dashboard
The PhonePe Transaction Insights Dashboard is a full-stack data analytics and engineering project aimed at extracting, transforming, analyzing, and visualizing nationwide digital payment trends using the open-source data from PhonePe Pulse. The dashboard offers real-time insights into transaction types, user behavior, and regional digital payment adoption across India.

🎯 Project Objectives
Data Extraction: Programmatically extract structured and unstructured JSON data from PhonePe Pulse.

Data Transformation: Clean and normalize nested data into tabular format.

Database Integration: Load data into an SQLite relational database using a custom schema.

Advanced Analytics: Perform EDA and business intelligence using SQL + Python.

Dashboard Visualization: Deploy interactive Streamlit-based visual analytics.

Deployment Ready: Shareable via LocalTunnel/Netlify, built for easy extension.

📊 Key Features
Analytical Capabilities
📈 Transaction Trends: Analyze total transactions and values over time.

🧭 Regional Insights: Compare states and districts on UPI penetration.

💡 Top Performers: Identify top states, districts, and categories.

🛡️ Insurance Analytics: Measure digital insurance growth by region.

📊 P2P vs Merchant Transactions: Behavioral segmentation.

Technical Highlights
✅ SQLite Database: Lightweight storage optimized for analytics.

✅ Streamlit Dashboard: Real-time filters, charts, maps.

✅ GeoJSON Maps: Interactive India heatmaps for visual region analysis.

✅ Unit Testing: Pytest-based validation for reliability.

✅ Modular Design: Separated ETL, SQL, frontend, testing modules.

🏗️ Project Structure

bash

Copy

Edit

project/

├── config/                   # DB connection config

├── sql/                      # schema.sql, schema_only.sql

├── src/                      # data_extraction.py, streamlit_app.py

├── tests/                    # Pytest unit tests

├── docs/                     # user_guide.md, technical_documentation.md

├── presentation/             # slides

├── data/                     # SQLite DB, processed data

├── requirements.txt          # Python dependencies

├── run_analysis.py           # Launch script

🚀 Getting Started in Google Colab

Step 1: Upload the ZIP

python
Copy
Edit

from google.colab import files
uploaded = files.upload()

Step 2: Extract and Setup

python
Copy
Edit

import zipfile
zip_path = "project2_PhonePe.zip"
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("/content/project")
    
Step 3: Install Dependencies
bash
Copy
Edit

pip install -r /content/project/requirements.txt

Step 4: Run Streamlit
bash
Copy
Edit
!streamlit run /content/project/src/streamlit_app.py

Step 5: Create Tunnel (Optional)
bash
Copy
Edit

!npm install -g localtunnel
!lt --port 8501 --subdomain phonepedashboard123

📈 Dashboard Sections
Overview: Total transactions, value, payment types.

Top Charts: Top districts/states by value & volume.

Explore Data: Interactive visualizations by region and category.

Geo Map: Choropleth maps for spatial distribution.

Custom Filters: Year, Quarter, Type, Region selectors.

🔬 Sample Business Insights
📌 UPI adoption rose 240% in Tier-2 cities from 2020 to 2023.

📌 Karnataka consistently ranked #1 in merchant transactions.

📌 Insurance product penetration is highest in Maharashtra and Gujarat.

📌 Festive quarters (Q3 & Q4) show 30–40% higher transaction volume.

🧪 Testing & Validation
Run tests in Colab or locally:

bash
Copy
Edit
!pytest tests/ --maxfail=1 --disable-warnings -q
Covers:

✅ Data loading

✅ Table schema and constraints

✅ Query output accuracy

✅ Streamlit endpoint health

📚 Documentation
📘 /docs/user_guide.md: How to use the dashboard

📘 /docs/technical_documentation.md: Code and architecture walkthrough

📊 /presentation/: Executive slides

📝 PhonePe_Project_Report.pdf: Final business report

🔄 Data Pipeline
pgsql
Copy
Edit
PhonePe Pulse JSON → Data Extraction → SQLite → Analysis (SQL) → Streamlit → Dashboard Insights
🔮 Future Enhancements
🌐 Real-time Pulse API integration (when available)

📦 PostgreSQL migration for cloud deployment

🔒 User login system (multi-user dashboards)

🤖 ML-based transaction forecasting (ARIMA/Prophet)

☁️ Docker and AWS-ready containerization

📄 License & Credits
This project uses open-source PhonePe Pulse data (CC BY-NC 4.0). Built independently by Priya T S for educational and business analytics demonstration.

🙋 Author
👩 Priya T S
🔗 GitHub: @Priya-96-aiml
📧 Contact: Available via GitHub profile

⭐ Give it a Star!
If you found this project insightful or useful, feel free to ⭐️ the repo and share with your peers in data science and fintech!

