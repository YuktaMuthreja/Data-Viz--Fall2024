import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def patient_dashboard():
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Patient Dashboard")
    data = pd.read_csv('healthcare_dataset 2.csv')
    st.write("Kindly any ID from the main dashboard page.")

    # Add a text input box for ID
    patient_id = st.text_input("Enter Patient ID:")

    # Filter data based on ID
    if patient_id:
        filtered_data = data[data['ID'] == patient_id]

        if not filtered_data.empty:
            # Display patient basic information
            st.subheader(f"Patient Information for ID: {patient_id}")
            patient_info = filtered_data.iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Name: {patient_info['Name']}")
                st.write(f"Age: {patient_info['Age']}")
                st.write(f"Gender: {patient_info['Gender']}")
                st.write(f"Blood Type: {patient_info['Blood Type']}")
                st.write(f"Medical Condition: {patient_info['Medical Condition']}")
            
            with col2:
                st.write(f"Doctor: {patient_info['Doctor']}")
                st.write(f"Hospital: {patient_info['Hospital Names']}")
                st.write(f"Insurance: {patient_info['Insurance Provider']}")
                st.write(f"Room Number: {patient_info['Room Number']}")
                st.write(f"Admission Type: {patient_info['Admission Type']}")

            # Visit History
            st.subheader("Visit History")
            visits_df = filtered_data[['Date of Admission', 'Discharge Date', 'Medical Condition', 
                                     'Doctor', 'Room Number', 'Medication', 'Test Results']]
            st.write(visits_df)

            # Calculate statistics
            num_visits = len(filtered_data)
            total_billing = filtered_data['Billing Amount'].sum()
            avg_stay_length = (pd.to_datetime(filtered_data['Discharge Date']) - 
                             pd.to_datetime(filtered_data['Date of Admission'])).mean().days

            # Display statistics
            st.subheader("Patient Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Number of Visits", num_visits)
            with col2:
                st.metric("Total Billing", f"${total_billing:,.2f}")
            with col3:
                st.metric("Average Stay (Days)", f"{avg_stay_length:.1f}")

            # Medical History Analysis
            st.subheader("Medical History Analysis")
            
            # Create a bar chart for medications
            med_counts = filtered_data['Medication'].value_counts()
            fig, ax = plt.subplots()
            med_counts.plot(kind='bar')
            plt.title('Medication History')
            plt.xlabel('Medication')
            plt.ylabel('Frequency')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Test Results Distribution
            st.subheader("Test Results Distribution")
            test_results = filtered_data['Test Results'].value_counts()
            st.bar_chart(test_results)

        else:
            st.warning("No patient found with the given ID.")

# Run the dashboard function
if __name__ == '__main__':
    patient_dashboard()
