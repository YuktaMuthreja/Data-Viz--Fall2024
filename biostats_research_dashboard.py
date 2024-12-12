import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config at the very beginning
#st.set_page_config(layout="wide")

def biostats_research_dashboard():
    #st.title("Advanced Hospital Analytics Dashboard")
    
    data = pd.read_csv('healthcare_dataset 2.csv')
    
    # Data preprocessing
    data['Billing Amount'] = pd.to_numeric(data['Billing Amount'], errors='coerce')
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'])
    data['Discharge Date'] = pd.to_datetime(data['Discharge Date'])
    data['Length of Stay'] = (data['Discharge Date'] - data['Date of Admission']).dt.days
    
    # # 1. Hospital Performance Radar Chart
    # st.header("Hospital Performance Multi-Metric Analysis")
    
    # metrics = {
    #     'Success_Rate': data.groupby('Hospital Names')['Test Results'].apply(lambda x: (x == 'Normal').mean() * 100),
    #     'Avg_Stay': data.groupby('Hospital Names')['Length of Stay'].mean(),
    #     'Avg_Cost': data.groupby('Hospital Names')['Billing Amount'].mean(),
    #     'Patient_Volume': data.groupby('Hospital Names').size()
    # }
    
    # # Normalize metrics for radar chart
    # hospital_metrics = pd.DataFrame(metrics)
    # for column in hospital_metrics.columns:
    #     hospital_metrics[column] = (hospital_metrics[column] - hospital_metrics[column].min()) / \
    #                              (hospital_metrics[column].max() - hospital_metrics[column].min())
    
    # fig1, ax1 = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    # angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
    # angles = np.concatenate((angles, [angles[0]]))  # complete the circle
    
    # for hospital in hospital_metrics.index:
    #     values = hospital_metrics.loc[hospital].values
    #     values = np.concatenate((values, [values[0]]))
    #     ax1.plot(angles, values, 'o-', linewidth=2, label=hospital)
    #     ax1.fill(angles, values, alpha=0.25)
    
    # ax1.set_xticks(angles[:-1])
    # ax1.set_xticklabels(metrics.keys())
    # ax1.set_title('Hospital Performance Metrics Comparison')
    # ax1.legend(bbox_to_anchor=(1.3, 1.0))
    # st.pyplot(fig1)
    # plt.close(fig1)

    # 2. Bubble Plot: Cost vs Stay Duration vs Patient Volume
    st.header("Cost, Stay Duration, and Patient Volume Analysis")
    
    hospital_stats = pd.DataFrame({
        'Avg_Cost': data.groupby('Hospital Names')['Billing Amount'].mean(),
        'Avg_Stay': data.groupby('Hospital Names')['Length of Stay'].mean(),
        'Patient_Count': data.groupby('Hospital Names').size()
    })
    
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    scatter = ax2.scatter(hospital_stats['Avg_Cost'], 
                         hospital_stats['Avg_Stay'],
                         s=hospital_stats['Patient_Count']/10,  # Size based on patient count
                         alpha=0.6,
                         c=range(len(hospital_stats)),  # Color gradient
                         cmap='viridis')
    
    # Add hospital labels
    for idx, hospital in enumerate(hospital_stats.index):
        ax2.annotate(hospital, 
                    (hospital_stats['Avg_Cost'][idx], hospital_stats['Avg_Stay'][idx]),
                    xytext=(5, 5), textcoords='offset points')
    
    ax2.set_xlabel('Average Cost ($)')
    ax2.set_ylabel('Average Length of Stay (days)')
    ax2.set_title('Hospital Performance Bubble Plot')
    
    # Add colorbar legend
    plt.colorbar(scatter, label='Hospital Index')
    st.pyplot(fig2)
    plt.close(fig2)

    # 3. Treatment Efficiency Analysis
    st.header("Treatment Efficiency Analysis")

    # Calculate efficiency ratio (Length of Stay / Billing Amount)
    data['Efficiency Ratio'] = data['Length of Stay'] / (data['Billing Amount'] / 1000)

    fig3, ax3b = plt.subplots(1, 1, figsize=(10, 6))

    # Efficiency by Hospital
    efficiency_by_hospital = data.groupby('Hospital Names')['Efficiency Ratio'].mean().sort_values()
    sns.barplot(x=efficiency_by_hospital.values, y=efficiency_by_hospital.index, ax=ax3b, palette='coolwarm')
    ax3b.set_title('Treatment Efficiency by Hospital')
    ax3b.set_xlabel('Efficiency Ratio')

    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # 2. Average Billing Amount by Medical Condition and Admission Type
    st.header("Average Billing Amount by Medical Condition and Admission Type")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    avg_billing = data.groupby(['Medical Condition', 'Admission Type'])['Billing Amount'].mean().unstack()
    sns.heatmap(avg_billing, annot=True, fmt=',.0f', cmap='YlOrRd')
    ax2.set_title('Average Billing Amount ($) by Medical Condition and Admission Type')
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    plt.close(fig2)

    # # 4. Medical Condition Network
    # st.header("Hospital-Condition Treatment Network")
    
    # condition_matrix = pd.crosstab(data['Hospital Names'], data['Medical Condition'])
    # condition_corr = condition_matrix.T.corr()
    
    # fig4, ax4 = plt.subplots(figsize=(12, 8))
    # mask = np.triu(np.ones_like(condition_corr))
    # sns.heatmap(condition_corr, mask=mask, annot=True, cmap='RdYlBu', center=0,
    #             square=True, fmt='.2f', cbar_kws={'label': 'Correlation'})
    # ax4.set_title('Hospital Treatment Pattern Correlations')
    # st.pyplot(fig4)
    # plt.close(fig4)

    # # 5. Time Series Analysis
    # st.header("Hospital Admission Patterns Over Time")
    
    # daily_admissions = data.groupby(['Date of Admission', 'Hospital Names']).size().unstack()
    
    # fig5, ax5 = plt.subplots(figsize=(15, 8))
    # for hospital in daily_admissions.columns:
    #     ax5.plot(daily_admissions.index, daily_admissions[hospital], 
    #             label=hospital, alpha=0.7, marker='o', markersize=4)
    
    # ax5.set_xlabel('Date')
    # ax5.set_ylabel('Number of Admissions')
    # ax5.set_title('Daily Admission Patterns by Hospital')
    # ax5.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # st.pyplot(fig5)
    # plt.close(fig5)

if __name__ == '__main__':
    biostats_research_dashboard()