# 🎯 Customer Intelligence Dashboard

An advanced, ML-powered customer analytics dashboard built with Python, Streamlit, Pandas, Plotly, and Scikit-learn. This dashboard performs automated customer segmentation using K-Means clustering and provides comprehensive business intelligence insights.

## 📊 Overview

The Customer Intelligence Dashboard is a modern business intelligence application that analyzes customer behavior, demographics, and spending patterns using unsupervised machine learning. It automatically segments customers into distinct groups based on Age, Income Level, and Coverage Amount, providing actionable insights for business strategy.

---

## ✨ Key Features

### 1. **🎯 KPI Cards**
- Total Customers & % of Database
- Average Income with Standard Deviation
- Average Spending Score
- Number of Customer Segments
- Average Customer Value

### 2. **👨‍👩‍👧‍👦 Customer Demographics**
- Age Distribution (Interactive Histogram)
- Gender Distribution (Pie Chart)
- Income Distribution (Histogram)

### 3. **💳 Spending Behavior Analysis**
- Income vs Spending Score (Interactive Scatter with bubble size)
- Age vs Spending Behavior (Interactive 3D Analysis)
- Premium Amount Distribution by Segment (Box Plot)
- Coverage Amount Distribution by Segment (Box Plot)

### 4. **🤖 Machine Learning Section**
- **Automated K-Means Clustering** on Age, Income, and Coverage Amount
- **Elbow Method** for optimal cluster detection
- **3D Cluster Visualization** for multi-dimensional analysis
- **Cluster Quality Metrics** and distribution analysis

### 5. **📋 Customer Segment Profiles**
- Automated segment identification
- Detailed segment characteristics:
  - Gender distribution
  - Average age, income, and spending
  - Customer value classification
  - Income segment classification
  - Spending profile analysis

### 6. **⚙️ Interactive Filters**
- Gender filter (multi-select)
- Age range slider
- Income level range slider
- Spending score range slider
- Segment selection filter
- **Real-time dashboard updates** on filter changes

### 7. **📈 Advanced Analytics**
- Top occupations analysis
- Customer distribution by segment and gender (Sunburst chart)
- Education level vs spending behavior analysis
- Occupational segmentation

### 8. **💾 Data Export & Insights**
- **CSV Export** - Download filtered dataset
- **Excel Export** - Multi-sheet workbook with filtered data and segment summary
- Strategic recommendations
- Action items for business teams

### 9. **🎨 Professional Design**
- Modern gradient backgrounds
- Color-coded visualizations
- Responsive layout
- Smooth interactive charts with hover tooltips
- Clean, intuitive navigation

---

## 🛠️ Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Interactive web framework & UI |
| **Pandas** | Data manipulation & preprocessing |
| **Plotly** | Interactive visualizations & charts |
| **Scikit-learn** | Machine learning (K-Means clustering) |
| **NumPy & SciPy** | Numerical computations |
| **Openpyxl** | Excel file generation |

---

## 📋 Data Processing Pipeline

### Data Preprocessing
1. **Handle Missing Values** - Impute numeric columns with median
2. **Data Type Conversion** - Ensure proper numeric types
3. **Normalization** - StandardScaler for clustering features
4. **Feature Engineering**:
   - `Spending_Score` - Normalized coverage amount (0-100)
   - `Premium_to_Income_Ratio` - Financial health indicator
   - `Customer_Value` - Total customer worth

### Machine Learning Pipeline
1. **Feature Selection**: Age, Income Level, Coverage Amount
2. **Standardization**: StandardScaler normalization
3. **Optimal Cluster Detection**: Elbow Method (K=2 to K=10)
4. **K-Means Clustering**: Final segmentation
5. **Cluster Analysis**: Segment profiling & insights

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download Project
```bash
cd /Users/bjaydhillon/Downloads/retaildashboard
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare Data
Ensure `customer_segmentation_data.csv` is in the project directory:
```
retaildashboard/
├── app.py                               # Main dashboard application
├── customer_segmentation_data.csv       # Customer data
├── requirements.txt                     # Python dependencies
└── README.md                           # This file
```

### Step 5: Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

---

## 📊 Dataset Structure

**File**: `customer_segmentation_data.csv`

| Column | Type | Description |
|--------|------|-------------|
| Customer ID | Integer | Unique customer identifier |
| Age | Integer | Customer age in years |
| Gender | String | Male/Female |
| Marital Status | String | Single/Married/Widowed/Divorced/Separated |
| Education Level | String | High School/Associate/Bachelor's/Master's/Doctorate |
| Geographic Information | String | State/Region |
| Occupation | String | Customer's job title |
| Income Level | Numeric | Annual income in ₹ |
| Behavioral Data | String | Policy/Behavior category |
| Purchase History | Date | Last purchase date |
| Interactions with Customer Service | String | Contact method |
| Insurance Products Owned | String | Product codes |
| Coverage Amount | Numeric | Insurance coverage in ₹ |
| Premium Amount | Numeric | Annual premium in ₹ |
| Policy Type | String | Individual/Family/Group/Business |
| Customer Preferences | String | Communication preference |
| Preferred Communication Channel | String | Email/Phone/Chat/etc |
| Preferred Contact Time | String | Morning/Afternoon/Evening/Anytime/Weekends |
| Preferred Language | String | English/French/German/Spanish/Mandarin |
| Segmentation Group | String | Pre-existing segment (Segment1-5) |

---

## 📈 Dashboard Sections Explained

### KPI Metrics
Quick overview of key business metrics with contextual statistics:
- **Total Customers**: Count of customers in filtered dataset
- **Average Income**: Mean income with standard deviation
- **Spending Score**: Normalized metric (0-100) indicating purchase propensity
- **Segments**: Number of distinct customer clusters
- **Customer Value**: Sum of Coverage + Premium (lifetime value indicator)

### Demographic Analysis
Understand customer base composition:
- **Age Distribution**: Identify age cohorts
- **Gender Mix**: Understand gender composition
- **Income Levels**: See wealth distribution

### Spending Behavior
Analyze purchase and engagement patterns:
- **Income vs Spending**: Correlation analysis
- **Age vs Spending**: Lifecycle spending patterns
- **Box Plots**: Identify outliers and distributions by segment

### ML Segmentation
Automated customer grouping:
- **Elbow Method**: Visual identification of optimal clusters
- **3D Visualization**: Multi-dimensional cluster representation
- **Cluster Metrics**: Size, characteristics, and profitability

### Segment Profiles
Detailed customer group analysis:
- Demographic breakdown
- Financial metrics
- Behavioral patterns
- Strategic segment identifiers (High-value, Budget, etc.)

---

## 🎯 Use Cases

### 1. **Customer Acquisition**
Target specific demographic segments with tailored marketing campaigns

### 2. **Revenue Optimization**
Identify high-value customers and premium segments for focus

### 3. **Risk Management**
Monitor low-value segments and develop retention strategies

### 4. **Product Development**
Design offerings aligned with segment preferences and income levels

### 5. **Customer Service**
Allocate resources based on segment communication preferences

### 6. **Financial Planning**
Forecast revenue based on segment size and customer value

---

## 🔧 Customization Guide

### Modify Clustering Features
Edit the `perform_clustering()` function to use different features:
```python
features = ['Age', 'Income Level', 'Premium Amount']  # Change these
```

### Adjust Number of Clusters
In the `perform_clustering()` function, adjust K_range:
```python
K_range = range(2, 15)  # Increase max for more granular clusters
```

### Change Filter Options
Modify the sidebar filter creation in the main code to add/remove filters

### Customize Colors
Replace color schemes in Plotly charts:
```python
color_discrete_sequence=px.colors.qualitative.Set2  # Change color palette
```

### Add New Visualizations
Create additional Plotly charts using the filtered_df DataFrame

---

## 📊 Interpretation Guide

### Customer Segments

**High-Value Customers**
- High Income Level
- High Spending Score
- Premium Products Owned
- Action: Premium support, exclusive offerings

**Budget Customers**
- Low-Medium Income
- Lower Spending Score
- Basic Products
- Action: Volume-based campaigns

**Potential Loyal Customers**
- Mid-Range Income & Spending
- Regular Interactions
- Multiple Products
- Action: Loyalty programs, cross-sell

**Emerging Customers**
- Young customers with growth potential
- Action: Development programs, investments

---

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Add Customer Intelligence Dashboard"
git push origin main
```

2. **Deploy on Streamlit Cloud**
- Go to [streamlit.io/cloud](https://streamlit.io/cloud)
- Connect your GitHub repository
- Select `app.py` as the entry file
- Deploy!

### Docker Deployment (Optional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

---

## 🔍 Troubleshooting

### Issue: "FileNotFoundError: customer_segmentation_data.csv"
**Solution**: Verify the CSV file is in the project directory

### Issue: "ModuleNotFoundError"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Dashboard loads slowly
**Solution**: Data is cached using `@st.cache_data`; clear cache with `streamlit cache clear`

### Issue: Filters not updating
**Solution**: Try browser refresh or restart Streamlit (`Ctrl+C` and `streamlit run app.py`)

---

## 📊 Performance Tips

1. **For Large Datasets** (>100k rows):
   - Filter data in SQL before loading
   - Use data sampling for visualizations
   - Increase caching duration

2. **Optimize Clustering**:
   - Reduce K_range for faster computation
   - Use n_init=5 instead of 10 for quick previews

3. **Improve Interactivity**:
   - Reduce number of points in scatter plots
   - Use session state for filter persistence

---

## 📝 License

This project is provided as-is for educational and business intelligence purposes.

---

## 👨‍💼 Support & Feedback

For issues or suggestions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Consult Scikit-learn clustering guide

---

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Scikit-learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

<div align="center">

**🚀 Customer Intelligence Dashboard**

*Advanced ML-Powered Business Analytics*

**Built with ❤️ using Streamlit, Scikit-learn & Plotly**

</div>