import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    # Read the CSV content from the provided string
    data = pd.read_csv('healthcare_dataset_preprocessed.csv')
    
    # Convert date columns
    date_cols = ['date_of_admission', 'discharge_date']
    for col in date_cols:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')
    
    return data

df = load_data()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .nav-button {
        width: 100%;
        margin: 0.5rem 0;
        padding: 0.75rem;
        font-size: 1.1rem;
    }
    .section-title {
        color: #2c3e50;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation system
def create_navigation():
    st.sidebar.markdown("## 🧭 Navigation")
    
    # Navigation buttons
    pages = {
        "🏠 Home": "home",
        "📊 General Analysis": "general",
        "🏥 Clinical Analysis": "clinical",
        "💰 Financial Analysis": "financial"
    }
    
    selected_page = st.sidebar.radio(
        "Go to:",
        list(pages.keys()),
        label_visibility="collapsed"
    )
    
    # Add filters to sidebar for relevant pages
    st.sidebar.markdown("---")
    
    if pages[selected_page] in ["general", "clinical", "financial"]:
        st.sidebar.markdown("### 🎯 Filters")
        
        # Date range filter
        min_date = df['date_of_admission'].min()
        max_date = df['date_of_admission'].max()
        
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = df[(df['date_of_admission'] >= pd.Timestamp(start_date)) & 
                            (df['date_of_admission'] <= pd.Timestamp(end_date))]
        else:
            filtered_df = df.copy()
        
        # Gender filter
        genders = ["All"] + list(df['gender'].unique())
        selected_gender = st.sidebar.selectbox("Gender", genders)
        
        if selected_gender != "All":
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
        
        # Hospital filter for financial page
        if pages[selected_page] == "financial":
            hospitals = ["All"] + list(df['hospital'].unique())
            selected_hospital = st.sidebar.selectbox("Hospital", hospitals)
            
            if selected_hospital != "All":
                filtered_df = filtered_df[filtered_df['hospital'] == selected_hospital]
        
        return pages[selected_page], filtered_df
    
    return pages[selected_page], df

# Page 1: Home / Overview
def home_page():
    st.markdown('<h1 class="main-header">🏥 Healthcare Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Patient, Clinical, and Financial Insights</h2>', unsafe_allow_html=True)
    
    # Introduction card
    with st.container():
        st.markdown("""
        <div class="card">
        <h3>📋 Project Overview</h3>
        <p>This interactive dashboard provides comprehensive insights into healthcare data, including 
        patient demographics, medical conditions, hospital performance, and healthcare costs. 
        Designed to support data-driven decision-making for healthcare administrators, clinicians, 
        and financial analysts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>👥 Total Patients</h3>
        <h2>{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>🏥 Hospitals</h3>
        <h2>{df['hospital'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        date_range = f"{df['date_of_admission'].min().year} - {df['date_of_admission'].max().year}"
        st.markdown(f"""
        <div class="metric-card">
        <h3>📅 Period</h3>
        <h2>{date_range}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
        <h3>🩺 Conditions</h3>
        <h2>{df['medical_condition'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation section
    st.markdown("---")
    st.markdown('<h2 class="section-title">🔍 Explore Dashboard Sections</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True, disabled=True):
            pass
        st.markdown("**Current Page**")
        st.markdown("Project overview and navigation")
    
    with col2:
        if st.button("📊 General Analysis", use_container_width=True):
            st.session_state.page = "general"
            st.rerun()
        st.markdown("**Patient Demographics**")
        st.markdown("Age, gender, time trends")
    
    with col3:
        if st.button("🏥 Clinical Analysis", use_container_width=True):
            st.session_state.page = "clinical"
            st.rerun()
        st.markdown("**Medical Insights**")
        st.markdown("Conditions, length of stay")
    
    with col4:
        if st.button("💰 Financial Analysis", use_container_width=True):
            st.session_state.page = "financial"
            st.rerun()
        st.markdown("**Cost Analysis**")
        st.markdown("Billing, hospital performance")

# Page 2: General Analysis
def general_analysis_page(filtered_df):
    st.markdown('<h1 class="main-header">📊 General Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Patient Demographics & Overview</h2>', unsafe_allow_html=True)
    
    # KPI Row
    st.markdown('<h3 class="section-title">📈 Key Performance Indicators</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_age = filtered_df['age'].mean()
        st.metric("Average Age", f"{avg_age:.1f} years")
    
    with col2:
        avg_stay = filtered_df['length_of_stay'].mean()
        st.metric("Avg Length of Stay", f"{avg_stay:.1f} days")
    
    with col3:
        total_billing = filtered_df['billing_amount'].sum()
        st.metric("Total Billing", f"${total_billing:,.0f}")
    
    with col4:
        patients_per_hospital = len(filtered_df) / filtered_df['hospital'].nunique()
        st.metric("Patients per Hospital", f"{patients_per_hospital:.0f}")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 👥 Age Distribution")
        # Create age groups
        bins = [0, 18, 30, 45, 60, 100]
        labels = ['0-18', '19-30', '31-45', '46-60', '60+']
        filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels, right=False)
        
        age_dist = filtered_df['age_group'].value_counts().sort_index()
        fig1 = px.bar(
            x=age_dist.index, 
            y=age_dist.values,
            labels={'x': 'Age Group', 'y': 'Number of Patients'},
            color=age_dist.values,
            color_continuous_scale='Blues'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("##### ♀️♂️ Gender Distribution")
        gender_dist = filtered_df['gender'].value_counts()
        fig2 = px.pie(
            values=gender_dist.values, 
            names=gender_dist.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🩸 Blood Type Distribution")
        blood_dist = filtered_df['blood_type'].value_counts()
        fig3 = px.bar(
            x=blood_dist.index, 
            y=blood_dist.values,
            labels={'x': 'Blood Type', 'y': 'Number of Patients'},
            color=blood_dist.values,
            color_continuous_scale='Reds'
        )
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("##### 📅 Monthly Admissions Trend")
        # Resample by month
        monthly_data = filtered_df.set_index('date_of_admission').resample('M').size()
        fig4 = px.line(
            x=monthly_data.index, 
            y=monthly_data.values,
            labels={'x': 'Date', 'y': 'Number of Admissions'},
            line_shape='spline'
        )
        fig4.update_traces(line=dict(width=3, color='#1f77b4'))
        st.plotly_chart(fig4, use_container_width=True)
    
    # Data table
    st.markdown('<h3 class="section-title">📋 Sample Data</h3>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df[['name', 'age', 'gender', 'medical_condition', 'hospital', 'date_of_admission']].head(10),
        use_container_width=True
    )

# Page 3: Clinical Analysis
def clinical_analysis_page(filtered_df):
    st.markdown('<h1 class="main-header">🏥 Clinical Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Medical Conditions & Patient Care Metrics</h2>', unsafe_allow_html=True)
    
    # Medical Conditions Analysis
    st.markdown('<h3 class="section-title">🩺 Medical Conditions Overview</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📊 Patients per Medical Condition")
        condition_dist = filtered_df['medical_condition'].value_counts()
        fig1 = px.bar(
            y=condition_dist.index, 
            x=condition_dist.values,
            orientation='h',
            labels={'x': 'Number of Patients', 'y': 'Medical Condition'},
            color=condition_dist.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("##### 🎯 Conditions Share (Treemap)")
        fig2 = px.treemap(
            filtered_df, 
            path=['medical_condition'],
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Length of Stay Analysis
    st.markdown('<h3 class="section-title">⏱️ Length of Stay Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Average Stay by Condition")
        avg_stay_by_condition = filtered_df.groupby('medical_condition')['length_of_stay'].mean().sort_values()
        fig3 = px.bar(
            y=avg_stay_by_condition.index, 
            x=avg_stay_by_condition.values,
            orientation='h',
            labels={'x': 'Average Length of Stay (days)', 'y': 'Medical Condition'},
            color=avg_stay_by_condition.values,
            color_continuous_scale='Blues'
        )
        fig3.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("##### 📊 Stay Distribution")
        # Create box plot for stay distribution
        fig4 = px.box(
            filtered_df, 
            x='medical_condition', 
            y='length_of_stay',
            points=False,
            color='medical_condition',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig4.update_layout(
            height=400,
            xaxis_title="Medical Condition",
            yaxis_title="Length of Stay (days)",
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Age vs Condition Analysis
    st.markdown('<h3 class="section-title">👵 Age Groups & Medical Conditions</h3>', unsafe_allow_html=True)
    
    # Create age groups
    bins = [0, 30, 50, 70, 100]
    labels = ['<30', '30-50', '50-70', '70+']
    filtered_df['age_category'] = pd.cut(filtered_df['age'], bins=bins, labels=labels, right=False)
    
    condition_by_age = pd.crosstab(filtered_df['age_category'], filtered_df['medical_condition'])
    
    fig5 = px.bar(
        condition_by_age,
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'value': 'Number of Patients', 'age_category': 'Age Group'}
    )
    fig5.update_layout(height=500)
    st.plotly_chart(fig5, use_container_width=True)
    
    # Test Results Analysis
    if 'test_results' in filtered_df.columns:
        st.markdown('<h3 class="section-title">🧪 Test Results Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_results = filtered_df['test_results'].value_counts()
            fig6 = px.pie(
                values=test_results.values,
                names=test_results.index,
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig6.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            test_by_condition = pd.crosstab(filtered_df['medical_condition'], filtered_df['test_results'])
            fig7 = px.imshow(
                test_by_condition,
                labels=dict(x="Test Result", y="Medical Condition", color="Count"),
                color_continuous_scale='YlOrRd'
            )
            st.plotly_chart(fig7, use_container_width=True)

# Page 4: Financial Analysis
def financial_analysis_page(filtered_df):
    st.markdown('<h1 class="main-header">💰 Financial & Operational Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Healthcare Costs & Hospital Performance</h2>', unsafe_allow_html=True)
    
    # Financial KPIs
    st.markdown('<h3 class="section-title">💵 Financial Key Performance Indicators</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_billing = filtered_df['billing_amount'].sum()
        st.metric("Total Billing Amount", f"${total_billing:,.0f}")
    
    with col2:
        avg_billing = filtered_df['billing_amount'].mean()
        st.metric("Average per Patient", f"${avg_billing:,.0f}")
    
    with col3:
        billing_per_day = total_billing / filtered_df['length_of_stay'].sum() if filtered_df['length_of_stay'].sum() > 0 else 0
        st.metric("Billing per Patient-Day", f"${billing_per_day:,.0f}")
    
    with col4:
        patients_per_condition = len(filtered_df) / filtered_df['medical_condition'].nunique()
        st.metric("Patients per Condition", f"{patients_per_condition:.0f}")
    
    # Hospital Performance
    st.markdown('<h3 class="section-title">🏥 Hospital Performance Comparison</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 💰 Which hospitals generate the highest costs?")
        billing_by_hospital = filtered_df.groupby('hospital')['billing_amount'].sum().sort_values(ascending=False).head(10)
        fig1 = px.bar(
            x=billing_by_hospital.values,
            y=billing_by_hospital.index,
            orientation='h',
            labels={'x': 'Total Billing Amount ($)', 'y': 'Hospital'},
            color=billing_by_hospital.values,
            color_continuous_scale='Reds'
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("##### ⏱️ Average Length of Stay by Hospital")
        stay_by_hospital = filtered_df.groupby('hospital')['length_of_stay'].mean().sort_values(ascending=False).head(10)
        fig2 = px.bar(
            x=stay_by_hospital.values,
            y=stay_by_hospital.index,
            orientation='h',
            labels={'x': 'Average Length of Stay (days)', 'y': 'Hospital'},
            color=stay_by_hospital.values,
            color_continuous_scale='Blues'
        )
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Insurance Analysis
    st.markdown('<h3 class="section-title">🛡️ Insurance Provider Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📊 Billing Distribution by Insurance")
        billing_by_insurance = filtered_df.groupby('insurance_provider')['billing_amount'].sum()
        fig3 = px.pie(
            values=billing_by_insurance.values,
            names=billing_by_insurance.index,
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.markdown("##### 👥 Patients per Insurance Provider")
        patients_by_insurance = filtered_df['insurance_provider'].value_counts()
        fig4 = px.bar(
            x=patients_by_insurance.index,
            y=patients_by_insurance.values,
            labels={'x': 'Insurance Provider', 'y': 'Number of Patients'},
            color=patients_by_insurance.values,
            color_continuous_scale='Greens'
        )
        fig4.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Time Trend Analysis
    st.markdown('<h3 class="section-title">📈 Monthly Billing Trend</h3>', unsafe_allow_html=True)
    
    # Create monthly billing trend
    filtered_df['admission_month'] = filtered_df['date_of_admission'].dt.to_period('M')
    monthly_billing = filtered_df.groupby('admission_month')['billing_amount'].sum()
    monthly_billing.index = monthly_billing.index.astype(str)
    
    fig5 = px.line(
        x=monthly_billing.index,
        y=monthly_billing.values,
        labels={'x': 'Month', 'y': 'Total Billing Amount ($)'},
        line_shape='spline',
        markers=True
    )
    fig5.update_traces(line=dict(width=3, color='#2ca02c'))
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)
    
    # Cost per Condition
    st.markdown('<h3 class="section-title">🏷️ Average Cost per Medical Condition</h3>', unsafe_allow_html=True)
    
    cost_by_condition = filtered_df.groupby('medical_condition')['billing_amount'].mean().sort_values(ascending=False)
    
    fig6 = px.bar(
        x=cost_by_condition.index,
        y=cost_by_condition.values,
        labels={'x': 'Medical Condition', 'y': 'Average Billing Amount ($)'},
        color=cost_by_condition.values,
        color_continuous_scale='Viridis'
    )
    fig6.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig6, use_container_width=True)
    
    # Room Number Analysis (if exists)
    if 'room_number' in filtered_df.columns:
        st.markdown('<h3 class="section-title">🚪 Room Utilization Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Most used rooms
            room_usage = filtered_df['room_number'].value_counts().head(10)
            fig7 = px.bar(
                x=room_usage.index.astype(str),
                y=room_usage.values,
                labels={'x': 'Room Number', 'y': 'Number of Admissions'},
                color=room_usage.values,
                color_continuous_scale='Purples'
            )
            st.plotly_chart(fig7, use_container_width=True)
        
        with col2:
            # Room vs Billing
            fig8 = px.scatter(
                filtered_df,
                x='room_number',
                y='billing_amount',
                color='medical_condition',
                labels={'room_number': 'Room Number', 'billing_amount': 'Billing Amount ($)'},
                opacity=0.7
            )
            st.plotly_chart(fig8, use_container_width=True)

# Main app logic
def main():
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Get navigation selection
    page, filtered_df = create_navigation()
    
    # Render the selected page
    if page == 'home':
        home_page()
    elif page == 'general':
        general_analysis_page(filtered_df)
    elif page == 'clinical':
        clinical_analysis_page(filtered_df)
    elif page == 'financial':
        financial_analysis_page(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>🏥 Healthcare Analytics Dashboard | Developed with Streamlit | Data Source: Healthcare Dataset</p>
        <p>For analytical and educational purposes only</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()