# E-Commerce Data Analysis Assessment - Dicoding

**Nama:** Junpito Salim
**Email:** [junpitosalim@gmail.com](mailto:junpitosalim@gmail.com)
**ID Dicoding:** 490585

## Deployed Link
E-Commerce Analytics Dashboard.

## Contents
- [Project Overview](#project-overview)
- [Structure of the Project](#structure-of-the-project)
- [How to Install](#how-to-install)
- [How to Use](#how-to-use)
- [Sources of Data](#sources-of-data)
- [Data Exploration](#data-exploration)
- [Data Visualization](#data-visualization)
- [Acknowledgements](#acknowledgements)

## Project Overview

This initiative focuses on analyzing and visualizing E-Commerce dataset from Brazilian Olist. It encompasses scripts for data preparation, exploratory analysis, and an interactive Streamlit dashboard for data visualization. The aim is to uncover patterns, connections, and trends in sales performance within specific variables, utilizing the available data from 2016-2018.

The project addresses key business questions:
- **Monthly Sales Trends**: How do sales patterns change over time?
- **Pareto Analysis**: Which product categories contribute most to revenue?
- **Payment Method Analysis**: How do customers prefer to pay and how it changes over time?

## Structure of the Project

```
data/: Folder with raw CSV data.
E_commerce_analisys.ipynb: Scripts for data cleaning, EDA, and analytical queries.
dashboard.py: Streamlit-based interactive dashboard.
README.md: Documentation of the project.
requirements.txt: Python dependencies.
```

## How to Install

Download the repository to your computer:
```bash
git clone https://github.com/junpito/E-commerce-dashboard.git
```

Install necessary Python packages using:
```bash
pip install -r requirements.txt
```

## How to Use

Data Preparation: The E_commerce_analisys.ipynb file includes scripts for data cleaning and preparation.

Data Exploration (EDA): Use the Python scripts provided for data analysis and exploration. Insights from EDA are vital for understanding the trends in sales performance.

Data Visualization: Execute the Streamlit dashboard for an interactive data visualization experience:
```bash
streamlit run dashboard.py
```
You can access the dashboard through [http://localhost:8501](http://localhost:8501) in your web browser.

## Sources of Data

The project utilizes E-Commerce data from the Brazilian E-Commerce Public Dataset by Olist (2016-2018), consisting of:
- **100k+ orders** from 2016 to 2018
- **Product categories** in Portuguese and English
- **Customer locations** with geolocation data
- **Payment methods** and review scores
- **Seller information** and product details

## Data Exploration

Detail the principal findings and insights obtained from the exploratory data analysis:

### Key Findings:
- **Monthly Sales Trends**: Identified seasonal patterns with peak sales in November-December
- **Pareto Analysis**: Top 5 product categories contribute to approximately 37% of total revenue
- **Payment Methods**: Credit card dominates with 75.6% market share, followed by boleto (20.3%)
- **Customer Satisfaction**: Average rating of 4.1/5.0 across all orders

### Business Insights:
- Health & Beauty category leads with $1.44M in revenue
- 80/20 rule confirmed: Top categories drive majority of sales
- Holiday seasons show 2x normal volume
- Steady growth from 2016-2018 with consistent seasonal patterns

## Data Visualization

Showcase the visual outputs produced by the Streamlit dashboard:

### Dashboard Features:
- **Interactive Filters**: Year and category selection
- **Monthly Trends**: Dual plot showing orders and revenue over time
- **Pareto Chart**: Full-width visualization of all product categories
- **Payment Analysis**: Treemap and heatmap visualizations
- **Key Metrics**: Real-time business KPIs display

### Visual Components:
- Line charts for trend analysis
- Bar charts for category comparison
- Treemaps for hierarchical data representation
- Heatmaps for temporal payment pattern analysis
- KPI cards for quick business insights

## Acknowledgements

This project was created as a part of the Dicoding Academy's "Belajar Analisis Data dengan Python" course, which focuses extensively on Python for data analysis. A heartfelt thank you to the Dicoding Academy for providing essential learning materials, support, and a learning platform.

Special thanks to:
- **Olist** for providing the Brazilian E-Commerce Public Dataset
- **Dicoding Indonesia** for the comprehensive data analysis curriculum
- **Streamlit** for the amazing dashboard framework
- **Plotly** for powerful data visualization capabilities
