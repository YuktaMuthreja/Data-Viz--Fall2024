import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

def main_dashboard():
    # Your main dashboard content goes here
    data = pd.read_csv('healthcare_dataset 2.csv')
    print(data.columns)

    # Rename columns to match the dataset description
    data.rename(columns={
        'Medication': 'Medication Prescribed',
        'Test Results': 'Outcome'
    }, inplace=True)

    st.sidebar.title('Dashboard Options')

    # Sidebar filter options
    selected_gender = st.sidebar.selectbox('Select Gender', data['Gender'].unique())
    selected_age = st.sidebar.slider('Select Age', float(data['Age'].min()), float(data['Age'].max()), (float(data['Age'].min()), float(data['Age'].max())))

    # Filter the data based on user selections
    filtered_data = data[(data['Gender'] == selected_gender) & (data['Age'] >= selected_age[0]) & (data['Age'] <= selected_age[1])]

    # Display the filtered data
    st.write('### Filtered Data')
    st.write(filtered_data)

    # Create a 2x2 grid layout for plots using subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

    # Plot 1: Bar chart
    axes[0, 0].set_title('Outcome Counts')
    bar_data = filtered_data['Outcome'].value_counts()
    bar_data.plot(kind='bar', ax=axes[0, 0], rot=0)
    axes[0, 0].set_ylabel('Count')

    # Plot 2: Histogram for Age
    axes[0, 1].set_title('Age Distribution')
    sns.histplot(data=filtered_data, x='Age', bins=20, kde=True, ax=axes[0, 1])
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Count')

    # Plot 3: Monthly admission count bar chart
    axes[1, 0].clear()  # Clear the previous messy plot
    axes[1, 0].set_title('Monthly Admission Count')

    # Resample data to monthly frequency and create bar chart
    line_data = filtered_data.groupby('Date of Admission').size().reset_index(name='Count')
    line_data['Date of Admission'] = pd.to_datetime(line_data['Date of Admission'])
    monthly_data = line_data.set_index('Date of Admission').resample('M')['Count'].sum().reset_index()

    # Create bar plot
    axes[1, 0].bar(monthly_data['Date of Admission'], 
                monthly_data['Count'],
                color='steelblue',
                alpha=0.7,
                width=20)  # Adjust width as needed

    # Format x-axis to show dates nicely
    axes[1, 0].xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show every 6 months
    axes[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(axes[1, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add labels and grid
    axes[1, 0].set_xlabel('Date of Admission')
    axes[1, 0].set_ylabel('Number of Admissions')
    axes[1, 0].grid(True, alpha=0.3, axis='y')

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Plot 4: Box plot for Age by Outcome
    axes[1, 1].set_title('Age Distribution by Outcome')
    sns.boxplot(x='Outcome', y='Age', data=filtered_data, ax=axes[1, 1])
    axes[1, 1].set_xlabel('Outcome')
    axes[1, 1].set_ylabel('Age')

    # Adjust layout
    plt.tight_layout()

    # Display the Matplotlib plot using Streamlit
    st.pyplot(fig)

# Run the Streamlit app
if __name__ == '__main__':
    main_dashboard()
