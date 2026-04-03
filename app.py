import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import io
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .segment-high {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
    }
    .segment-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
    }
    .segment-low {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
    }
    .dashboard-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading and Caching
@st.cache_data
def load_data():
    df = pd.read_csv('customer_segmentation_data.csv')
    return df

@st.cache_data
def preprocess_data(df):
    """
    Comprehensive data preprocessing
    """
    df = df.copy()
    
    # Handle missing values
    df['Income Level'] = pd.to_numeric(df['Income Level'], errors='coerce')
    df['Coverage Amount'] = pd.to_numeric(df['Coverage Amount'], errors='coerce')
    df['Premium Amount'] = pd.to_numeric(df['Premium Amount'], errors='coerce')
    
    # Fill missing values with median for numeric columns
    numeric_cols = ['Income Level', 'Coverage Amount', 'Premium Amount']
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    # Create derived metrics
    df['Spending_Score'] = (df['Coverage Amount'] / df['Coverage Amount'].max() * 100).round(2)
    df['Premium_to_Income_Ratio'] = (df['Premium Amount'] / (df['Income Level'] + 1) * 100).round(2)
    df['Customer_Value'] = (df['Coverage Amount'] + df['Premium Amount']).fillna(0)
    
    return df

@st.cache_data
def perform_clustering(df, n_clusters=None):
    """
    Perform K-Means clustering with Elbow Method
    """
    # Select features for clustering
    features = ['Age', 'Income Level', 'Coverage Amount']
    X = df[features].copy()
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Elbow Method to find optimal clusters
    inertias = []
    silhouette_scores = []
    K_range = range(2, 11)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    
    # Use optimal clusters (if not specified)
    if n_clusters is None:
        # Calculate elbow point
        n_clusters = 4  # Default
        for i in range(1, len(inertias) - 1):
            acceleration = (inertias[i-1] - inertias[i]) - (inertias[i] - inertias[i+1])
            threshold = (inertias[1] - inertias[0]) * 0.05
            if acceleration > threshold:
                n_clusters = i + 1
                break
    
    # Final clustering
    kmeans_final = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans_final.fit_predict(X_scaled)
    
    return clusters, kmeans_final, scaler, inertias, K_range

# Load and preprocess data
df = load_data()
df = preprocess_data(df)

# Theme selector in sidebar
theme = st.sidebar.radio("🎨 Theme", options=["Light", "Dark"])

# App Title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="dashboard-header">
        <h1>🎯 Customer Intelligence Dashboard</h1>
        <p style="font-size: 14px; margin-top: 0;">Advanced ML-Powered Customer Analytics & Segmentation</p>
    </div>
    """, unsafe_allow_html=True)

# Perform clustering
clusters, kmeans_model, scaler, inertias, K_range = perform_clustering(df)
df['Cluster'] = clusters

# ============================================================================
# SIDEBAR - INTERACTIVE FILTERS
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Filters & Controls")

# Gender filter
genders = st.sidebar.multiselect(
    "👥 Gender",
    options=sorted(df['Gender'].unique()),
    default=sorted(df['Gender'].unique())
)

# Age range filter
age_range = st.sidebar.slider(
    "📅 Age Range",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Income range filter
income_range = st.sidebar.slider(
    "💰 Income Level Range",
    min_value=int(df['Income Level'].min()),
    max_value=int(df['Income Level'].max()),
    value=(int(df['Income Level'].min()), int(df['Income Level'].max()))
)

# Spending Score filter
spending_range = st.sidebar.slider(
    "🛍️ Spending Score Range",
    min_value=0.0,
    max_value=100.0,
    value=(0.0, 100.0)
)

# Cluster filter
clusters_list = sorted(df['Cluster'].unique())
selected_clusters = st.sidebar.multiselect(
    "🔬 Customer Segments",
    options=clusters_list,
    default=clusters_list
)

# Apply filters
filtered_df = df[
    (df['Gender'].isin(genders)) &
    (df['Age'] >= age_range[0]) &
    (df['Age'] <= age_range[1]) &
    (df['Income Level'] >= income_range[0]) &
    (df['Income Level'] <= income_range[1]) &
    (df['Spending_Score'] >= spending_range[0]) &
    (df['Spending_Score'] <= spending_range[1]) &
    (df['Cluster'].isin(selected_clusters))
]

# ============================================================================
# SECTION 1: KPI CARDS
# ============================================================================
st.markdown("### 📊 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.metric(
        label="👥 Total Customers",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df)/len(df)*100:.1f}% of database"
    )

with kpi_col2:
    st.metric(
        label="💰 Avg Income",
        value=f"₹{filtered_df['Income Level'].mean():,.0f}",
        delta=f"₹{filtered_df['Income Level'].std():,.0f} std dev"
    )

with kpi_col3:
    st.metric(
        label="🛍️ Avg Spending Score",
        value=f"{filtered_df['Spending_Score'].mean():.1f}",
        delta=f"Range: {filtered_df['Spending_Score'].min():.1f} - {filtered_df['Spending_Score'].max():.1f}"
    )

with kpi_col4:
    st.metric(
        label="🔬 Number of Segments",
        value=f"{len(filtered_df['Cluster'].unique())}",
        delta=f"{len(selected_clusters)} selected"
    )

with kpi_col5:
    st.metric(
        label="💎 Avg Customer Value",
        value=f"₹{filtered_df['Customer_Value'].mean():,.0f}",
        delta=f"Total: ₹{filtered_df['Customer_Value'].sum():,.0f}"
    )

st.markdown("---")

# ============================================================================
# SECTION 2: CUSTOMER DEMOGRAPHICS
# ============================================================================
st.markdown("### 👨‍👩‍👧‍👦 Customer Demographics")
demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    # Age Distribution
    fig_age = px.histogram(
        filtered_df,
        x='Age',
        nbins=30,
        title='Age Distribution',
        color_discrete_sequence=['#667eea'],
        labels={'Age': 'Age (years)', 'count': 'Number of Customers'},
        opacity=0.7
    )
    fig_age.update_layout(height=400, showlegend=False, hovermode='x')
    st.plotly_chart(fig_age, use_container_width=True)

with demo_col2:
    # Gender Distribution
    gender_counts = filtered_df['Gender'].value_counts()
    fig_gender = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        title='Gender Distribution',
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
    )
    fig_gender.update_layout(height=400)
    st.plotly_chart(fig_gender, use_container_width=True)

with demo_col3:
    # Income Distribution
    fig_income = px.histogram(
        filtered_df,
        x='Income Level',
        nbins=30,
        title='Income Distribution',
        color_discrete_sequence=['#764ba2'],
        labels={'Income Level': 'Income Level (₹)', 'count': 'Number of Customers'},
        opacity=0.7
    )
    fig_income.update_layout(height=400, showlegend=False, hovermode='x')
    st.plotly_chart(fig_income, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 3: SPENDING BEHAVIOR
# ============================================================================
st.markdown("### 💳 Spending Behavior Analysis")
spending_col1, spending_col2 = st.columns(2)

with spending_col1:
    # Income vs Spending Score Scatter
    fig_scatter = px.scatter(
        filtered_df,
        x='Income Level',
        y='Spending_Score',
        color='Cluster',
        size='Premium Amount',
        hover_name='Customer ID',
        hover_data={'Income Level': ':,.0f', 'Spending_Score': ':.1f', 'Cluster': True},
        title='Income vs Spending Score (Bubble size = Premium Amount)',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'Income Level': 'Income Level (₹)', 'Spending_Score': 'Spending Score'}
    )
    fig_scatter.update_layout(height=450, hovermode='closest')
    st.plotly_chart(fig_scatter, use_container_width=True)

with spending_col2:
    # Age vs Spending Score
    fig_age_spending = px.scatter(
        filtered_df,
        x='Age',
        y='Spending_Score',
        color='Cluster',
        size='Customer_Value',
        hover_name='Customer ID',
        hover_data={'Age': True, 'Spending_Score': ':.1f', 'Cluster': True},
        title='Age vs Spending Behavior (Bubble size = Customer Value)',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'Age': 'Age (years)', 'Spending_Score': 'Spending Score'}
    )
    fig_age_spending.update_layout(height=450, hovermode='closest')
    st.plotly_chart(fig_age_spending, use_container_width=True)

# Spending Distribution
spending_col3, spending_col4 = st.columns(2)

with spending_col3:
    fig_spending_dist = px.box(
        filtered_df,
        x='Cluster',
        y='Premium Amount',
        color='Cluster',
        title='Premium Amount Distribution by Segment',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'Cluster': 'Customer Segment', 'Premium Amount': 'Premium Amount (₹)'}
    )
    fig_spending_dist.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_spending_dist, use_container_width=True)

with spending_col4:
    fig_coverage_dist = px.box(
        filtered_df,
        x='Cluster',
        y='Coverage Amount',
        color='Cluster',
        title='Coverage Amount Distribution by Segment',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={'Cluster': 'Customer Segment', 'Coverage Amount': 'Coverage Amount (₹)'}
    )
    fig_coverage_dist.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_coverage_dist, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 4: MACHINE LEARNING SECTION - CLUSTERING
# ============================================================================
st.markdown("### 🤖 Machine Learning: Customer Segmentation")

ml_col1, ml_col2 = st.columns(2)

with ml_col1:
    # Elbow Method Visualization
    fig_elbow = go.Figure()
    fig_elbow.add_trace(go.Scatter(
        x=list(K_range),
        y=inertias,
        mode='lines+markers',
        marker=dict(size=10, color='#667eea'),
        line=dict(width=3, color='#667eea'),
        name='Inertia'
    ))
    fig_elbow.update_layout(
        title='Elbow Method for Optimal Clusters',
        xaxis_title='Number of Clusters (K)',
        yaxis_title='Inertia (Within-cluster sum of squares)',
        hovermode='x',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

with ml_col2:
    # Cluster distribution
    cluster_counts = filtered_df['Cluster'].value_counts().sort_index()
    fig_cluster_dist = px.bar(
        x=cluster_counts.index,
        y=cluster_counts.values,
        title='Customer Distribution Across Segments',
        labels={'x': 'Customer Segment', 'y': 'Number of Customers'},
        color=cluster_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_cluster_dist.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_cluster_dist, use_container_width=True)

# 3D Cluster Visualization
fig_3d = px.scatter_3d(
    filtered_df,
    x='Age',
    y='Income Level',
    z='Spending_Score',
    color='Cluster',
    hover_name='Customer ID',
    size='Customer_Value',
    title='3D Customer Segmentation Visualization',
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={'Age': 'Age', 'Income Level': 'Income (₹)', 'Spending_Score': 'Spending Score'}
)
fig_3d.update_layout(height=500, hovermode='closest')
st.plotly_chart(fig_3d, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 5: CUSTOMER SEGMENT PROFILES
# ============================================================================
st.markdown("### 📋 Customer Segment Profiles & Insights")

# Create segment insights
segment_insights = []
for cluster_id in sorted(filtered_df['Cluster'].unique()):
    cluster_data = filtered_df[filtered_df['Cluster'] == cluster_id]
    
    insight = {
        'Segment': f'Segment {cluster_id}',
        'Customer Count': len(cluster_data),
        'Avg Age': f"{cluster_data['Age'].mean():.1f}",
        'Avg Income': f"₹{cluster_data['Income Level'].mean():,.0f}",
        'Avg Spending Score': f"{cluster_data['Spending_Score'].mean():.1f}",
        'Avg Coverage': f"₹{cluster_data['Coverage Amount'].mean():,.0f}",
        'Avg Premium': f"₹{cluster_data['Premium Amount'].mean():,.0f}",
        'Total Value': f"₹{cluster_data['Customer_Value'].sum():,.0f}"
    }
    segment_insights.append(insight)

insights_df = pd.DataFrame(segment_insights)

# Display insights table
st.dataframe(insights_df, use_container_width=True, hide_index=True)

# Detailed segment analysis
st.markdown("#### 🔍 Detailed Segment Analysis")

segment_tabs = st.tabs([f"Segment {i}" for i in sorted(filtered_df['Cluster'].unique())])

for idx, cluster_id in enumerate(sorted(filtered_df['Cluster'].unique())):
    with segment_tabs[idx]:
        cluster_data = filtered_df[filtered_df['Cluster'] == cluster_id]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Customers", f"{len(cluster_data):,}")
        with col2:
            st.metric("Avg Age", f"{cluster_data['Age'].mean():.0f} yrs")
        with col3:
            st.metric("Avg Income", f"₹{cluster_data['Income Level'].mean():,.0f}")
        with col4:
            st.metric("Avg Spending", f"{cluster_data['Spending_Score'].mean():.1f}")
        
        # Segment characteristics
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
            **📊 Segment Characteristics:**
            - **Male/Female Ratio:** {(cluster_data['Gender'].value_counts().get('Male', 0) / len(cluster_data) * 100):.1f}% / {(cluster_data['Gender'].value_counts().get('Female', 0) / len(cluster_data) * 100):.1f}%
            - **Most Common Occupation:** {cluster_data['Occupation'].mode()[0] if len(cluster_data['Occupation'].mode()) > 0 else 'N/A'}
            - **Most Common Marital Status:** {cluster_data['Marital Status'].mode()[0] if len(cluster_data['Marital Status'].mode()) > 0 else 'N/A'}
            - **Income Range:** ₹{cluster_data['Income Level'].min():,.0f} - ₹{cluster_data['Income Level'].max():,.0f}
            """)
        
        with col_b:
            st.markdown(f"""
            **💡 Segment Insights:**
            - **Spending Profile:** {'High' if cluster_data['Spending_Score'].mean() > filtered_df['Spending_Score'].quantile(0.66) else 'Medium' if cluster_data['Spending_Score'].mean() > filtered_df['Spending_Score'].quantile(0.33) else 'Low'} Spenders
            - **Customer Value:** {'Premium' if cluster_data['Customer_Value'].mean() > filtered_df['Customer_Value'].quantile(0.66) else 'Standard' if cluster_data['Customer_Value'].mean() > filtered_df['Customer_Value'].quantile(0.33) else 'Value'} Customers
            - **Income Segment:** {'High Income' if cluster_data['Income Level'].mean() > filtered_df['Income Level'].quantile(0.66) else 'Mid Income' if cluster_data['Income Level'].mean() > filtered_df['Income Level'].quantile(0.33) else 'Low Income'}
            - **Age Group:** {'Senior (50+)' if cluster_data['Age'].mean() > 50 else 'Mid-aged (35-50)' if cluster_data['Age'].mean() > 35 else 'Young (< 35)'}
            """)
        
        st.markdown("---")

st.markdown("---")

# ============================================================================
# SECTION 6: ADVANCED ANALYTICS
# ============================================================================
st.markdown("### 📈 Advanced Analytics")

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:
    # Top occupations
    top_occupations = filtered_df['Occupation'].value_counts().head(10)
    fig_occupations = px.bar(
        x=top_occupations.values,
        y=top_occupations.index,
        orientation='h',
        title='Top 10 Occupations',
        labels={'x': 'Number of Customers', 'y': 'Occupation'},
        color=top_occupations.values,
        color_continuous_scale='Viridis'
    )
    fig_occupations.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_occupations, use_container_width=True)

with analytics_col2:
    # Customer segmentation distribution
    fig_seg_dist = px.sunburst(
        filtered_df,
        path=['Cluster', 'Gender'],
        title='Customer Distribution: Segment → Gender',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_seg_dist.update_layout(height=400)
    st.plotly_chart(fig_seg_dist, use_container_width=True)

# Education Level vs Spending
fig_education = px.box(
    filtered_df,
    x='Education Level',
    y='Spending_Score',
    color='Cluster',
    title='Education Level vs Spending Behavior',
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={'Education Level': 'Education', 'Spending_Score': 'Spending Score'}
)
fig_education.update_layout(height=400, xaxis_tickangle=45)
st.plotly_chart(fig_education, use_container_width=True)

st.markdown("---")

# ============================================================================
# SECTION 7: DATA EXPORT & INSIGHTS
# ============================================================================
st.markdown("### 💾 Export & Recommendations")

export_col1, export_col2 = st.columns(2)

with export_col1:
    st.subheader("📥 Download Filtered Data")
    
    # CSV Export
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📊 Download CSV",
        data=csv,
        file_name="customer_intelligence_filtered.csv",
        mime="text/csv"
    )
    
    # Excel Export
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, sheet_name='Filtered Data', index=False)
        insights_df.to_excel(writer, sheet_name='Segment Summary', index=False)
    
    excel_buffer.seek(0)
    st.download_button(
        label="📈 Download Excel",
        data=excel_buffer,
        file_name="customer_intelligence.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with export_col2:
    st.subheader("💡 Strategic Recommendations")
    st.markdown("""
    **🎯 Key Action Items:**
    
    1. **High-Value Customer Retention** - Focus on segments with highest customer value
    2. **Personalized Marketing** - Tailor campaigns based on segment demographics
    3. **Income-based Offerings** - Create products aligned with income segments
    4. **Behavioral Targeting** - Use spending patterns for targeted promotions
    5. **Risk Management** - Identify and manage low-value customer segments
    
    **📊 Dashboard Benefits:**
    - Real-time customer insights
    - ML-powered segmentation
    - Data-driven decision making
    - Automated customer profiling
    """)

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div style='text-align: center; padding: 20px; color: gray;'>
    <p>🚀 <strong>Customer Intelligence Dashboard</strong> | Powered by Streamlit, Scikit-learn & Plotly</p>
    <p>Last Updated: 2026 | Data Points: {:,} | Segments: {}</p>
</div>
""".format(len(df), len(df['Cluster'].unique())), unsafe_allow_html=True)
