import numpy as np
import streamlit as st
import pandas as pd

def queuing_analysis(lambda_val, mu_val, server_count, system_limit, source_limit):
    # Kode untuk analisis antrian
    pass

def cpm_calculation(tasks):
    dependencies = {}
    durations = {}
    earliest_start = {}
    earliest_finish = {}
    latest_start = {}
    latest_finish = {}
    slack = {}
    critical_path = []

    for task in tasks:
        from_node, to_node, activity_symbol, duration = task
        if from_node not in dependencies:
            dependencies[from_node] = []
        dependencies[from_node].append(to_node)
        durations[from_node] = duration

    # Menghitung earliest start dan earliest finish time
    def calculate_earliest_times(node):
        if node not in earliest_start:
            earliest_start[node] = 0
            earliest_finish[node] = durations[node]
            if node in dependencies:
                for dependency in dependencies[node]:
                    earliest_finish[node] += calculate_earliest_times(dependency)
                    earliest_start[node] = max(earliest_start[node], earliest_finish[dependency])
        return earliest_finish[node]

    # Menghitung latest start dan latest finish time
    def calculate_latest_times(node, end_time):
        if node not in latest_finish:
            latest_finish[node] = end_time
            latest_start[node] = latest_finish[node] - durations[node]
            if node in dependencies:
                for dependency in dependencies[node]:
                    calculate_latest_times(dependency, latest_start[node])
                    latest_start[node] = min(latest_start[node], latest_start[dependency] - durations[node])
                    latest_finish[node] = latest_start[node] + durations[node]
        return latest_start[node]

    # Menghitung slack time
    def calculate_slack(node):
        if node not in slack:
            slack[node] = latest_start[node] - earliest_start[node]
            if node in dependencies:
                for dependency in dependencies[node]:
                    calculate_slack(dependency)
                    slack[node] = min(slack[node], slack[dependency])
        return slack[node]

    # Mencari critical path
    def find_critical_path(node):
        critical_path.append(node)
        if node in dependencies:
            for dependency in dependencies[node]:
                if slack[dependency] == 0:
                    find_critical_path(dependency)

    # Memanggil fungsi-fungsi perhitungan CPM
    for node in dependencies:
        calculate_earliest_times(node)

    for node in dependencies:
        calculate_latest_times(node, earliest_finish[node])

    for node in dependencies:
        calculate_slack(node)

    for node in dependencies:
        if slack[node] == 0:
            find_critical_path(node)

    # Menampilkan hasil perhitungan CPM dalam bentuk tabel
    df = pd.DataFrame(columns=['Activity', 'Earliest Start', 'Earliest Finish', 'Latest Start', 'Latest Finish', 'Slack'])
    for task in tasks:
        from_node, to_node, activity_symbol, duration = task
        df = df.append({'Activity': activity_symbol,
                        'Earliest Start': earliest_start[from_node],
                        'Earliest Finish': earliest_finish[from_node],
                        'Latest Start': latest_start[from_node],
                        'Latest Finish': latest_finish[from_node],
                        'Slack': slack[from_node]}, ignore_index=True)

    st.write("\nCritical Path Method (CPM) Calculation Results:")
    st.write(df)

    st.write("\nCritical Path:")
    st.write(" -> ".join(critical_path))

# Tampilan program menggunakan Streamlit
st.title('QUEUING ANALYSIS AND CRITICAL PATH METHOD CALCULATION')
st.text('Note : CPM yang dapat dihitung hanya bisa dalam bentuk sederhana saja')

analysis_type = st.selectbox("Analysis Type:", options=["Queuing Analysis", "CPM Calculation"])

if analysis_type == "Queuing Analysis":
    lambda_val = st.number_input("Lambda (Arrival rate):", min_value=0.0, value=1.0)
    mu_val = st.number_input("Mu (Service rate):", min_value=0.0, value=1.0)
    server_count = st.number_input("Number of Servers:", min_value=1, value=1)
    system_limit = st.selectbox("System Limit:", options=["Infinite", 0, 1, 2, 3, 4, 5])
    source_limit = st.selectbox("Source Limit:", options=["Infinite", 0, 1, 2, 3, 4, 5])

    if st.button("Run Analysis"):
        queuing_analysis(lambda_val, mu_val, server_count, system_limit, source_limit)

elif analysis_type == "CPM Calculation":
    task_rows = st.number_input("Number of Tasks:", min_value=1, value=1, step=1)
    tasks = []
    for i in range(task_rows):
        from_node = st.text_input(f"From Node {i+1}:")
        to_node = st.text_input(f"To Node {i+1}:")
        activity_symbol = st.text_input(f"Activity Symbol {i+1}:")
        duration = st.number_input(f"Duration {i+1}:", min_value=0, value=0, step=1)
        tasks.append((from_node, to_node, activity_symbol, duration))

    if st.button("Run Calculation"):
        cpm_calculation(tasks)
