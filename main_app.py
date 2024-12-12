import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from main_dashboard import main_dashboard
from financial_dashboard import financial_dashboard
from patient_dashboard import patient_dashboard
from biostats_research_dashboard import biostats_research_dashboard
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set page title
st.set_page_config(page_title="Hospital Dashboard")

st.sidebar.title('Dashboard Navigation')
selected_option = st.sidebar.selectbox('Select a Dashboard', ['Hospital Statistics Dashboard', 'Main Dashboard', 'Financial Dashboard', 'Patient Dashboard', 'BioStats Research Dashboard'])

# Create a function to display the selected dashboard content
def display_dashboard():
    if selected_option == 'Hospital Statistics Dashboard':
        st.subheader('Welcome to the Hospital Dashboard!')
        st.write("Welcome to the Hospital Dashboard—a comprehensive platform designed to provide actionable insights into hospital operations, patient care, and resource management. This dashboard offers an intuitive interface to explore key metrics such as patient demographics, admission trends, and outcome analysis, empowering stakeholders to make data-driven decisions.")
        
        # Load data
        data = pd.read_csv('healthcare_dataset 2.csv')

        # Convert date columns to datetime format
        data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')
        data['Discharge Date'] = pd.to_datetime(data['Discharge Date'], errors='coerce')

        # Sidebar filters
        st.sidebar.title("Filters")
        age_range = st.sidebar.slider(
            "Select Age Range", 
            min_value=int(data['Age'].min()), 
            max_value=int(data['Age'].max()), 
            value=(20, 60)
        )
        selected_gender = st.sidebar.multiselect(
            "Select Gender", 
            options=data['Gender'].unique(), 
            default=data['Gender'].unique()
        )
        selected_hospitals = st.sidebar.multiselect(
            "Select Hospital(s)", 
            options=data['Hospital Names'].unique(), 
            default=data['Hospital Names'].unique()
        )
        selected_month = st.sidebar.selectbox(
            "Select Month",
            options=["Overall"] + list(range(1, 13)),  # Adding 'Overall' option
            index=0
        )

        # Apply filters
        filtered_data = data[
            (data['Age'] >= age_range[0]) & 
            (data['Age'] <= age_range[1]) & 
            (data['Gender'].isin(selected_gender)) & 
            (data['Hospital Names'].isin(selected_hospitals))
        ]

        # Apply month filter if not "Overall"
        if selected_month != "Overall":
            filtered_data = filtered_data[filtered_data['Date of Admission'].dt.month == selected_month]

        # Display filtered data preview for debugging
        st.write("Filtered Data Preview")
        st.write(filtered_data.head())

        # Display statistics
        st.title("Hospital Statistics")
        total_patients = len(filtered_data)
        emergency_count = len(filtered_data[filtered_data['Admission Type'] == 'Emergency'])
        urgent_count = len(filtered_data[filtered_data['Admission Type'] == 'Urgent'])
        elective_count = len(filtered_data[filtered_data['Admission Type'] == 'Elective'])

        col1, col2, col3, col4 = st.columns(4)

        # Define a function to create a decorated box
        def create_box(title, value, col):
            box_style = "border: 2px solid #4682B4; border-radius: 10px; padding: 10px; background-color: #E0EBF5; width: 150px; height:150px;"
            col.markdown(
                f"""
                <div style="{box_style}">
                    <h3 style="color: #4682B4;">{title}</h3>
                    <p style="font-size: 20px; font-weight: bold; color: #1E90FF;">{value}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Display statistics boxes
        create_box("Total Patients", total_patients, col1)
        create_box("Emergency Count", emergency_count, col2)
        create_box("Urgent Count", urgent_count, col3)
        create_box("Elective Count", elective_count, col4)

        # Medical Condition Tree Plot
        st.title("Medical Condition Statistics")
        medical_condition_counts = filtered_data['Medical Condition'].value_counts().head(7).reset_index()
        medical_condition_counts.columns = ['Medical Condition', 'Count']
        fig_tree = px.treemap(
            medical_condition_counts,
            path=['Medical Condition'],
            values='Count',
            color='Count',
            color_continuous_scale='darkmint',
            labels={'Count': 'Frequency'}
        )
        st.plotly_chart(fig_tree, use_container_width=True)

        # Admission Type Distribution
        st.title("Admission Type Distribution")
        admission_counts = filtered_data['Admission Type'].value_counts().reset_index()
        admission_counts.columns = ['Admission Type', 'Count']
        fig_admission = px.bar(admission_counts, x='Admission Type', y='Count', text='Count', template="seaborn")
        fig_admission.update_traces(textposition='outside')
        fig_admission.update_layout(yaxis_title="Count", xaxis_title="Admission Type")
        st.plotly_chart(fig_admission, use_container_width=True)

        # Age Distribution
        st.title("Age Distribution")
        fig_age = px.histogram(
            filtered_data,
            x='Age',
            nbins=10,
            title="Filtered Age Distribution of Patients",
            template='seaborn',
            labels={'Age': 'Patient Age'}
        )
        fig_age.update_layout(yaxis_title="Count", xaxis_title="Age")
        st.plotly_chart(fig_age, use_container_width=True)

        # Gender Distribution
        # st.title("Gender Distribution")
        # gender_counts = filtered_data['Gender'].value_counts().reset_index()
        # gender_counts.columns = ['Gender', 'Count']
        # fig_gender = px.bar(
        #     gender_counts,
        #     x='Gender',
        #     y='Count',
        #     text='Count',
        #     template='seaborn',
        #     title="Filtered Gender Distribution of Patients"
        # )
        # fig_gender.update_traces(textposition='outside')
        # fig_gender.update_layout(yaxis_title="Count", xaxis_title="Gender")
        # st.plotly_chart(fig_gender, use_container_width=True)

        # Medical Condition Tree Plot
        # st.title("Medical Condition Statistics")
        # medical_condition_counts = filtered_data['Medical Condition'].value_counts().head(7).reset_index()
        # medical_condition_counts.columns = ['Medical Condition', 'Count']
        # fig_tree = px.treemap(
        #     medical_condition_counts,
        #     path=['Medical Condition'],
        #     values='Count',
        #     color='Count',
        #     color_continuous_scale='darkmint',
        #     labels={'Count': 'Frequency'}
        # )
        # st.plotly_chart(fig_tree, use_container_width=True)

        # KDE Plot for Duration of Stay
        st.title('KDE Plot for Duration of Stay')
        filtered_data['Duration of Stay'] = (filtered_data['Discharge Date'] - filtered_data['Date of Admission']).dt.days
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(filtered_data['Duration of Stay'], color='blue', label='Duration of Stay', ax=ax)
        mean_duration_stay = filtered_data['Duration of Stay'].mean()
        ax.axvline(mean_duration_stay, color='blue', linestyle='dashed', linewidth=2, label=f'Mean: {mean_duration_stay:.2f} days')
        ax.legend()
        ax.set_title('Duration of Stay')
        ax.set_xlabel('Duration (Days)')
        ax.set_ylabel('Density')
        st.pyplot(fig)
    
    elif selected_option == 'Main Dashboard':
        st.subheader('Main Dashboard')
        st.write("The Main Dashboard provides an overview of key metrics and statistics related to hospital admissions.")
        st.write("Here are some features:")
        st.markdown("- **Patient Demographics:** Visualizations showcasing age distribution, gender ratios, etc.")
        st.markdown("- **Admission Trends:** Charts representing admission trends over time.")
        st.markdown("- **Outcome Analysis:** Insightful graphs on patient outcomes.")
        main_dashboard()

    elif selected_option == 'Financial Dashboard':
        st.subheader('Custom Dashboard')
        st.write("The Custom Dashboard allows you to perform detailed analyses based on your preferences.")
        st.write("Here's what you can do:")
        st.markdown("- **Univariate Analysis:** Explore individual variables with various chart options.")
        st.markdown("- **Bivariate Analysis:** Investigate relationships between two variables.")
        st.write("Choose your analysis type from the sidebar and dive into the data!")
        financial_dashboard()
    
    elif selected_option == 'Patient Dashboard':
        st.subheader('Patient Dashboard')
        st.write("The Patient Dashboard allows you to perform detailed analyses based on the patient ID.")
        st.write("Here's what you can do:")
        patient_dashboard()

    elif selected_option == 'BioStats Research Dashboard':
        st.subheader('Bio Stats  Dashboard')
        biostats_research_dashboard()

# Display the selected dashboard content
display_dashboard()

