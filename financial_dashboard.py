import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def financial_dashboard():
    st.title("Hospital Financial Analytics Dashboard")
    
    # Load and prepare data
    data = pd.read_csv('healthcare_dataset 2.csv')
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Hospital filter
    selected_hospitals = st.sidebar.multiselect(
        "Select Hospitals",
        options=sorted(data['Hospital Names'].unique()),
        default=data['Hospital Names'].unique()
    )
    
    # Dynamic insurance provider filter based on selected hospitals
    available_insurance = data[data['Hospital Names'].isin(selected_hospitals)]['Insurance Provider'].unique()
    selected_insurance = st.sidebar.multiselect(
        "Select Insurance Providers",
        options=sorted(available_insurance),
        default=available_insurance
    )
    
    # Filter the dataset
    filtered_data = data[
        (data['Hospital Names'].isin(selected_hospitals)) &
        (data['Insurance Provider'].isin(selected_insurance))
    ]
    
    # Display key metrics
    st.header("Key Financial Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_billing = filtered_data['Billing Amount'].sum()
        st.metric("Total Billing Amount", f"${total_billing:,.2f}")
    
    with col2:
        avg_billing = filtered_data['Billing Amount'].mean()
        st.metric("Average Bill per Patient", f"${avg_billing:,.2f}")
    
    with col3:
        total_patients = len(filtered_data)
        st.metric("Total Patients", total_patients)
    
    # Insurance Provider Analysis
    st.header("Insurance Provider Analysis")
    
        # Create insurance metrics using the filtered dataset
    insurance_metrics = filtered_data.groupby('Insurance Provider').agg({
        'Billing Amount': ['sum', 'mean'],
        'Name': 'count'
    }).round(2)
    insurance_metrics.columns = ['Total Revenue', 'Average Bill', 'Patient Count']
    insurance_metrics = insurance_metrics.reset_index()
    
    # Ensure Total Revenue is calculated correctly with filtered data
    insurance_metrics['Total Revenue'] = insurance_metrics['Patient Count'] * insurance_metrics['Average Bill']
    
    # Create treemap with filtered data
    fig_insurance = px.treemap(
        insurance_metrics,
        path=['Insurance Provider'],
        values='Patient Count',
        color='Average Bill',
        color_continuous_scale=['#f7fbff', '#4292c6'],  # Subtle blue scale
        color_continuous_midpoint=insurance_metrics['Average Bill'].median(),
        title='Insurance Provider Distribution',
        custom_data=['Total Revenue', 'Average Bill']
    )
    
    fig_insurance.update_layout(
        coloraxis_colorbar=dict(
            title="Average Bill ($)",
            tickformat="$,.0f"
        ),
        margin=dict(t=50, l=25, r=25, b=25)  # Adjust margins for better spacing
    )
    
    fig_insurance.update_traces(
        hovertemplate='<b>%{label}</b><br>' +
        'Patient Count: %{value}<br>' +
        'Total Revenue: $%{customdata[0]:,.2f}<br>' +
        'Average Bill: $%{customdata[1]:,.2f}<extra></extra>'
    )
    
    fig_insurance.update_layout(height=500)
    st.plotly_chart(fig_insurance)
    
    # Medical Condition Analysis
    st.header("Medical Condition Cost Analysis")
    
    condition_metrics = filtered_data.groupby('Medical Condition').agg({
        'Billing Amount': ['sum', 'mean'],
        'Name': 'count'
    }).round(2)
    condition_metrics.columns = ['Total Revenue', 'Average Bill', 'Patient Count']
    condition_metrics = condition_metrics.reset_index()
    condition_metrics = condition_metrics.sort_values('Total Revenue', ascending=True)
    
    # Create horizontal bar chart with subtle colors
    fig_conditions = go.Figure()
    fig_conditions.add_trace(go.Bar(
        y=condition_metrics['Medical Condition'],
        x=condition_metrics['Total Revenue'],
        orientation='h',
        marker_color=condition_metrics['Average Bill'],
        marker_colorscale='Tealrose',  # More subtle color scale
        text=[f'${x:,.0f}' for x in condition_metrics['Total Revenue']],
        textposition='auto',
        customdata=np.stack((
            condition_metrics['Patient Count'],
            condition_metrics['Average Bill']
        ), axis=-1)
    ))
    
    fig_conditions.update_layout(
        title='Medical Condition Revenue Analysis',
        xaxis_title='Total Revenue ($)',
        yaxis_title='Medical Condition',
        height=600,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0.9)',  # Lighter background
        paper_bgcolor='rgba(0,0,0,0.9)'
    )
    
    fig_conditions.update_traces(
        hovertemplate='<b>%{y}</b><br>' +
        'Total Revenue: $%{x:,.2f}<br>' +
        'Patient Count: %{customdata[0]}<br>' +
        'Average Bill: $%{customdata[1]:,.2f}<extra></extra>'
    )
    
    st.plotly_chart(fig_conditions)
    
    # Admission Type Analysis
    st.header("Admission Type Cost Analysis")
    
    admission_metrics = filtered_data.groupby('Admission Type').agg({
        'Billing Amount': ['mean', 'std', 'sum'],
        'Name': 'count'
    }).round(2)
    admission_metrics.columns = ['Average Bill', 'Std Dev', 'Total Revenue', 'Patient Count']
    admission_metrics = admission_metrics.reset_index()
    
    fig_box = go.Figure()
    
    colors = ['#a6cee3', '#b2df8a', '#fb9a99']  # Subtle pastel colors
    
    for idx, admission_type in enumerate(admission_metrics['Admission Type']):
        admission_data = filtered_data[filtered_data['Admission Type'] == admission_type]
        fig_box.add_trace(go.Box(
            y=admission_data['Billing Amount'],
            name=f"{admission_type}<br>({len(admission_data)} patients)",
            boxpoints='outliers',
            marker_color=colors[idx % len(colors)]
        ))
    
    fig_box.update_layout(
        title='Cost Distribution by Admission Type (with Patient Counts)',
        yaxis_title='Billing Amount ($)',
        height=500,
        plot_bgcolor='rgba(0,0,0,0.9)',
        paper_bgcolor='rgba(0,0,0,0.9)'
    )
    st.plotly_chart(fig_box)
    
    # Length of Stay Analysis
    st.header("Length of Stay Analysis")
    
    filtered_data['Date of Admission'] = pd.to_datetime(filtered_data['Date of Admission'])
    filtered_data['Discharge Date'] = pd.to_datetime(filtered_data['Discharge Date'])
    filtered_data['Length of Stay'] = (filtered_data['Discharge Date'] - filtered_data['Date of Admission']).dt.days
    
    # Create scatter plot with subtle colors
    fig_los = px.scatter(
        filtered_data,
        x='Length of Stay',
        y='Billing Amount',
        color='Medical Condition',
        size='Length of Stay',
        color_discrete_sequence=px.colors.qualitative.Pastel,  # Subtle pastel colors
        title='Billing Amount vs Length of Stay by Medical Condition',
        labels={'Length of Stay': 'Length of Stay (Days)', 'Billing Amount': 'Billing Amount ($)'},
        height=600
    )
    
    fig_los.update_layout(
        plot_bgcolor='rgba(0,0,0,0.9)',
        paper_bgcolor='rgba(0,0,0,0.9)'
    )
    
    st.plotly_chart(fig_los)
    
    correlation = filtered_data['Length of Stay'].corr(filtered_data['Billing Amount'])
    st.write(f"Correlation coefficient between Length of Stay and Billing Amount: {correlation:.2f}")

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    financial_dashboard()