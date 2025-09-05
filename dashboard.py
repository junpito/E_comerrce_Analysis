import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
 

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.markdown('<h1 class="main-header">🛒 E-Commerce Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Analisis Data E-Commerce Brazilian Olist Dataset (2016-2018)**")
st.markdown("*Junpito Salim - Dicoding Data Analytics Project*")
st.markdown("---")

def _validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame | None:
    """Validate required columns and coerce important dtypes."""
    required_cols = [
        'order_purchase_timestamp',
        'product_category_name_english',
        'order_id',
        'total_item_value',
        'review_score',
        'payment_type'
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Kolom wajib hilang: {missing}. Perbaiki file 'processed_main_df.csv'.")
        return None

    # Coerce types that will be used downstream
    df = df.copy()
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    df['total_item_value'] = pd.to_numeric(df['total_item_value'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
    # Drop rows with invalid timestamps
    df = df.dropna(subset=['order_purchase_timestamp'])
    return df

# Load data function
@st.cache_data
def load_data():
    """Load and prepare data for dashboard from default path."""
    path = 'data/processed_main_df.csv'
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Gagal membaca data: {e}")
        return None

    return _validate_and_prepare(df)

def render_dashboard(df: pd.DataFrame) -> None:
    """Render all dashboard sections given a valid dataframe."""
    # Prepare data for visualizations
    df['year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.year
    df['month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.month
    df['order_month_year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M')
    
    # Sidebar filters
    years = sorted(df['year'].dropna().unique())
    categories = sorted(df['product_category_name_english'].dropna().unique())
    
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=['All Years'] + [str(int(year)) for year in years],
        index=0
    )
    
    selected_category = st.sidebar.selectbox(
        "Select Category", 
        options=['All Categories'] + list(categories),
        index=0
    )
    
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_year != 'All Years':
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]
    
    # Key Metrics Row
    st.markdown("## 📊 Key Business Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = filtered_df['order_id'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col2:
        total_revenue = filtered_df['total_item_value'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    with col3:
        avg_order_value = filtered_df['total_item_value'].mean()
        st.metric("Avg Order Value", f"${avg_order_value:.2f}")
    
    with col4:
        avg_satisfaction = filtered_df['review_score'].mean()
        st.metric("Customer Satisfaction", f"{avg_satisfaction:.2f}/5.0")
    
    st.markdown("---")
    
    # Main Dashboard Grid - 2x2 Layout
    st.markdown("## 📈 Business Analysis Dashboard")
    
    # Row 1: Monthly Orders and Monthly Revenue side-by-side
    st.markdown("### 📈 Monthly Trends")
    col_mo, col_mr = st.columns(2)

    # Monthly aggregation
    monthly_sales = filtered_df.groupby(['year', 'month']).agg({
        'order_id': 'count',
        'total_item_value': 'sum'
    }).reset_index()

    with col_mo:
        fig_orders = go.Figure()
        if selected_year == 'All Years':
            for year in years:
                year_data = monthly_sales[monthly_sales['year'] == year]
                fig_orders.add_trace(go.Scatter(
                    x=year_data['month'],
                    y=year_data['order_id'],
                    mode='lines+markers',
                    name=str(int(year)),
                    line=dict(width=3)
                ))
        else:
            fig_orders.add_trace(go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['order_id'],
                mode='lines+markers',
                name='Orders',
                line=dict(width=3, color='#2ca02c')
            ))
        fig_orders.update_layout(
            title="Monthly Orders",
            xaxis_title="Month",
            yaxis_title="Orders",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_orders, use_container_width=True)

    with col_mr:
        fig_revenue = go.Figure()
        if selected_year == 'All Years':
            for year in years:
                year_data = monthly_sales[monthly_sales['year'] == year]
                fig_revenue.add_trace(go.Scatter(
                    x=year_data['month'],
                    y=year_data['total_item_value'],
                    mode='lines+markers',
                    name=str(int(year)),
                    line=dict(width=3)
                ))
        else:
            fig_revenue.add_trace(go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['total_item_value'],
                mode='lines+markers',
                name='Revenue',
                line=dict(width=3, color='#1f77b4')
            ))
        fig_revenue.update_layout(
            title="Monthly Revenue",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

    # Row 2: Pareto - full width
    st.markdown("### 📊 Pareto: Category Revenue")
    
    # Category revenue analysis
    if selected_category == 'All Categories':
        category_revenue = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False).head(10)
    else:
        # Show subcategory analysis or related categories
        category_revenue = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False).head(10)
    
    # Calculate cumulative percentage
    total_revenue_all = df['total_item_value'].sum()
    cumulative_pct = (category_revenue.cumsum() / total_revenue_all * 100)
    
    # Create Pareto chart
    fig2 = go.Figure()
    
    # Bar chart
    fig2.add_trace(go.Bar(
        x=category_revenue.index,
        y=category_revenue.values,
        name="Revenue",
        marker_color="skyblue",
        yaxis="y1"
    ))
    
    # Line chart for cumulative %
    fig2.add_trace(go.Scatter(
        x=category_revenue.index,
        y=cumulative_pct.values,
        mode="lines+markers",
        name="Cumulative %",
        yaxis="y2",
        line=dict(color="red", width=3)
    ))
    
    # Add 80% line
    fig2.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="80% Rule")
    
    fig2.update_layout(
        title="Top Categories Revenue Distribution",
        xaxis=dict(title="Product Category", tickangle=45),
        yaxis=dict(title="Revenue ($)", side="left"),
        yaxis2=dict(title="Cumulative %", overlaying="y", side="right"),
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Row 3: Payment Analysis (Treemap, Heatmap)
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 💳 Pertanyaan 3: Payment Method Distribution")
        
        # Get top categories for treemap
        top_categories = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False)
        cumulative_pct = (top_categories.cumsum() / top_categories.sum() * 100)
        top_80_categories = cumulative_pct[cumulative_pct <= 80].index.tolist()
        
        # Filter for top categories
        treemap_df = df[df['product_category_name_english'].isin(top_80_categories)]
        
        # Create treemap data
        treemap_data = treemap_df.groupby(['product_category_name_english', 'payment_type']).agg({
            'total_item_value': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        treemap_data.columns = ['Category', 'Payment_Method', 'Revenue', 'Order_Count']
        treemap_data['Revenue_Pct'] = (treemap_data['Revenue'] / treemap_data['Revenue'].sum() * 100).round(2)
        
        # Create treemap
        fig3 = px.treemap(
            treemap_data,
            path=['Category', 'Payment_Method'],
            values='Revenue',
            color='Revenue_Pct',
            color_continuous_scale='RdYlBu_r',
            title="Payment Methods by Category",
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.markdown("### 📅 Pertanyaan 4: Payment Trends Over Time")
        
        # Payment temporal analysis
        payment_pivot = pd.crosstab(
            df['order_month_year'].astype(str),
            df['payment_type'],
            normalize='index'
        ) * 100
        
        # Create heatmap using Plotly
        fig4 = go.Figure(data=go.Heatmap(
            z=payment_pivot.values,
            x=payment_pivot.columns,
            y=payment_pivot.index,
            colorscale='YlOrRd',
            showscale=True,
            hoverongaps=False
        ))
        
        fig4.update_layout(
            title="Payment Method Evolution Over Time (%)",
            xaxis_title="Payment Method",
            yaxis_title="Month-Year",
            height=400
        )
        
        st.plotly_chart(fig4, use_container_width=True)

# Sidebar for filters
st.sidebar.header("🔧 Dashboard Filters")
st.sidebar.markdown("Filter data untuk analisis yang lebih spesifik")

# Load data
df = load_data()

if df is not None:
    # Prepare data for visualizations
    df['year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.year
    df['month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.month
    df['order_month_year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M')
    
    # Sidebar filters
    years = sorted(df['year'].unique())
    categories = sorted(df['product_category_name_english'].unique())
    
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=['All Years'] + [str(year) for year in years],
        index=0
    )
    
    selected_category = st.sidebar.selectbox(
        "Select Category", 
        options=['All Categories'] + list(categories),
        index=0
    )
    
    # Filter data based on selections
    filtered_df = df.copy()
    if selected_year != 'All Years':
        filtered_df = filtered_df[filtered_df['year'] == int(selected_year)]
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['product_category_name_english'] == selected_category]
    
    # Key Metrics Row
    st.markdown("## 📊 Key Business Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = filtered_df['order_id'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col2:
        total_revenue = filtered_df['total_item_value'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    with col3:
        avg_order_value = filtered_df['total_item_value'].mean()
        st.metric("Avg Order Value", f"${avg_order_value:.2f}")
    
    with col4:
        avg_satisfaction = filtered_df['review_score'].mean()
        st.metric("Customer Satisfaction", f"{avg_satisfaction:.2f}/5.0")
    
    st.markdown("---")
    
    # Main Dashboard Grid - 2x2 Layout
    st.markdown("## 📈 Business Analysis Dashboard")
    
    # Row 1: Temporal Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Pertanyaan 1: Monthly Sales Trends")
        
        # Monthly sales aggregation
        monthly_sales = filtered_df.groupby(['year', 'month']).agg({
            'order_id': 'count',
            'total_item_value': 'sum'
        }).reset_index()
        
        # Create line chart
        fig1 = go.Figure()
        
        if selected_year == 'All Years':
            for year in years:
                year_data = monthly_sales[monthly_sales['year'] == year]
                fig1.add_trace(go.Scatter(
                    x=year_data['month'],
                    y=year_data['total_item_value'],
                    mode='lines+markers',
                    name=str(year),
                    line=dict(width=3)
                ))
        else:
            fig1.add_trace(go.Scatter(
                x=monthly_sales['month'],
                y=monthly_sales['total_item_value'],
                mode='lines+markers',
                name='Revenue',
                line=dict(width=3, color='#1f77b4')
            ))
        
        fig1.update_layout(
            title="Monthly Revenue Trends",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Pertanyaan 2: Category Revenue (Pareto)")
        
        # Category revenue analysis
        if selected_category == 'All Categories':
            category_revenue = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False).head(10)
        else:
            # Show subcategory analysis or related categories
            category_revenue = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False).head(10)
        
        # Calculate cumulative percentage
        total_revenue_all = df['total_item_value'].sum()
        cumulative_pct = (category_revenue.cumsum() / total_revenue_all * 100)
        
        # Create Pareto chart
        fig2 = go.Figure()
        
        # Bar chart
        fig2.add_trace(go.Bar(
            x=category_revenue.index,
            y=category_revenue.values,
            name="Revenue",
            marker_color="skyblue",
            yaxis="y1"
        ))
        
        # Line chart for cumulative %
        fig2.add_trace(go.Scatter(
            x=category_revenue.index,
            y=cumulative_pct.values,
            mode="lines+markers",
            name="Cumulative %",
            yaxis="y2",
            line=dict(color="red", width=3)
        ))
        
        # Add 80% line
        fig2.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="80% Rule")
        
        fig2.update_layout(
            title="Top Categories Revenue Distribution",
            xaxis=dict(title="Product Category", tickangle=45),
            yaxis=dict(title="Revenue ($)", side="left"),
            yaxis2=dict(title="Cumulative %", overlaying="y", side="right"),
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Payment Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 💳 Pertanyaan 3: Payment Method Distribution")
        
        # Get top categories for treemap
        top_categories = df.groupby('product_category_name_english')['total_item_value'].sum().sort_values(ascending=False)
        cumulative_pct = (top_categories.cumsum() / top_categories.sum() * 100)
        top_80_categories = cumulative_pct[cumulative_pct <= 80].index.tolist()
        
        # Filter for top categories
        treemap_df = df[df['product_category_name_english'].isin(top_80_categories)]
        
        # Create treemap data
        treemap_data = treemap_df.groupby(['product_category_name_english', 'payment_type']).agg({
            'total_item_value': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        treemap_data.columns = ['Category', 'Payment_Method', 'Revenue', 'Order_Count']
        treemap_data['Revenue_Pct'] = (treemap_data['Revenue'] / treemap_data['Revenue'].sum() * 100).round(2)
        
        # Create treemap
        fig3 = px.treemap(
            treemap_data,
            path=['Category', 'Payment_Method'],
            values='Revenue',
            color='Revenue_Pct',
            color_continuous_scale='RdYlBu_r',
            title="Payment Methods by Category",
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.markdown("### 📅 Pertanyaan 4: Payment Trends Over Time")
        
        # Payment temporal analysis
        payment_pivot = pd.crosstab(
            df['order_month_year'].astype(str),
            df['payment_type'],
            normalize='index'
        ) * 100
        
        # Create heatmap using Plotly
        fig4 = go.Figure(data=go.Heatmap(
            z=payment_pivot.values,
            x=payment_pivot.columns,
            y=payment_pivot.index,
            colorscale='YlOrRd',
            showscale=True,
            hoverongaps=False
        ))
        
        fig4.update_layout(
            title="Payment Method Evolution Over Time (%)",
            xaxis_title="Payment Method",
            yaxis_title="Month-Year",
            height=400
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # Additional Insights Section
    st.markdown("---")
    st.markdown("## 💡 Key Business Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Temporal Insights")
        st.info("""
        **Key Findings:**
        - Strong growth trajectory from 2016-2018
        - Seasonal patterns: Nov-Jan peak performance
        - Holiday season 2x normal volume
        - Stable mid-year baseline demand
        """)
        
        st.markdown("### 🏆 Category Insights")  
        st.success("""
        **Key Findings:**
        - Top 5 categories = 37.4% total revenue
        - Health & Beauty leads ($1.44M)
        - 80/20 rule confirmed
        - Long tail: 51 categories = 20% revenue
        """)
    
    with col2:
        st.markdown("### 💳 Payment Insights")
        st.warning("""
        **Key Findings:**
        - Credit card dominance: 75.6%
        - Boleto stable: 20.3% 
        - Digital payment growth trend
        - Category-specific preferences
        """)
        
        st.markdown("### 🎯 Strategic Recommendations")
        st.error("""
        **Action Items:**
        - Focus on top 10 categories (65% revenue)
        - Holiday campaign planning essential
        - Credit card optimization priority
        - Customer retention programs needed
        """)

else:
    # Instructions for data preparation
    st.markdown("## 📋 Setup Instructions")
    
    st.markdown("### Step 1: Export Data")
    st.code("""
    # Run this in your notebook to export data:
    main_df.to_csv('data/processed_main_df.csv', index=False)
    """)
    
    st.markdown("### Step 2: Run Dashboard")
    st.code("""
    # In terminal/command prompt:
    streamlit run dashboard.py
    """)
    
    st.info("After exporting the data, refresh this page to see the dashboard!")

# Footer
st.markdown("---")
st.markdown("**Dashboard created for Dicoding Data Analytics Submission | E-Commerce Analysis Project**")
