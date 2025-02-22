import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os

# Load datasets
emergency_data = pd.read_csv("emergency_data.csv")
hospital_data = pd.read_csv("hospital_data.csv")
supply_chain_data = pd.read_csv("supply_chain_data.csv")

# Load results.txt
with open("results.txt", "r") as f:
    content = f.read()

# Extract data using regex
import re
emergency_data_str = re.search(r"Emergency Data:\n(.*?)Hospital Data:", content, re.DOTALL).group(1).strip()
hospital_data_str = re.search(r"Hospital Data:\n(.*?)Supply Chain Data:", content, re.DOTALL).group(1).strip()
supply_chain_data_str = re.search(r"Supply Chain Data:\n(.*?)Optimal Assignment:", content, re.DOTALL).group(1).strip()
optimal_assignment_str = re.search(r"Optimal Assignment:\n(.*?)\nOptimal Total Cost:", content, re.DOTALL).group(1).strip()
optimal_cost_str = re.search(r"Optimal Total Cost: (.*?) km", content).group(1).strip()

# Convert string data to DataFrame
emergency_data = pd.read_csv(io.StringIO(emergency_data_str), delim_whitespace=True)
hospital_data = pd.read_csv(io.StringIO(hospital_data_str), delim_whitespace=True)
supply_chain_data = pd.read_csv(io.StringIO(supply_chain_data_str), delim_whitespace=True)

# Process optimal assignment
optimal_assignment = eval(optimal_assignment_str)
optimal_cost = float(optimal_cost_str)

# Streamlit UI
st.set_page_config(layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Cost Matrix", "Optimal Assignments", "Conclusion"])

st.title("Healthcare Logistics Optimization Dashboard")
st.write("This dashboard presents the results of a healthcare logistics optimization project using quantum computing techniques.")

if page == "Overview":
    st.subheader("Dataset Overview")
    dataset_choice = st.selectbox("Select Dataset", ["Emergency Data", "Hospital Data", "Supply Chain Data"])
    if dataset_choice == "Emergency Data":
        st.dataframe(emergency_data)
    elif dataset_choice == "Hospital Data":
        st.dataframe(hospital_data)
    else:
        st.dataframe(supply_chain_data)

elif page == "Cost Matrix":
    st.subheader("Cost Matrix Visualization")
    
    if not os.path.exists("cost_matrix.txt"):
        cost_matrix = np.random.randint(10, 100, size=(len(supply_chain_data), len(hospital_data)))
        np.savetxt("cost_matrix.txt", cost_matrix, fmt='%d')
    else:
        cost_matrix = np.loadtxt("cost_matrix.txt")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cost_matrix, annot=True, fmt=".1f", cmap='viridis', cbar_kws={'label': 'Cost (km)'})
    plt.xlabel("Hospitals")
    plt.ylabel("Supply Centers")
    plt.title("Cost Matrix: Distance Between Supply Centers and Hospitals")
    st.pyplot(fig)

elif page == "Optimal Assignments":
    st.subheader("Optimal Assignment Results")
    
    selected_supply_center = st.selectbox("Select Supply Center", ["All"] + [str(assignment[0]) for assignment in optimal_assignment])
    
    if selected_supply_center == "All":
        for assignment in optimal_assignment:
            st.write(f"Supply Center {assignment[0]} → Hospital {assignment[1]}")
    else:
        filtered_assignment = [assignment for assignment in optimal_assignment if str(assignment[0]) == selected_supply_center]
        for assignment in filtered_assignment:
            st.write(f"Supply Center {assignment[0]} → Hospital {assignment[1]}")
    
    st.write(f"**Optimal Total Cost:** {optimal_cost} km")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(8, 5))
    supply_centers = [a[0] for a in optimal_assignment]
    hospitals = [a[1] for a in optimal_assignment]
    ax.bar(supply_centers, hospitals, color='blue')
    plt.xlabel("Supply Centers")
    plt.ylabel("Assigned Hospitals")
    plt.title("Optimal Assignment Distribution")
    st.pyplot(fig)

elif page == "Conclusion":
    st.subheader("Conclusion")
    st.write("""
        The optimization of healthcare logistics is crucial for ensuring timely access to medical supplies and improving patient care quality. 
        By utilizing quantum computing methods, we can enhance decision-making processes in healthcare logistics, leading to more efficient operations 
        and better patient outcomes.
    """)

