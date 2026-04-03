import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Leave Management System", layout="wide")
st.title("Leave Management System")

menu = st.sidebar.selectbox("Select Role", ["Employee", "Admin"])

if menu == "Employee":
    st.header("Employee Panel")

    tab1, tab2, tab3 = st.tabs(["Add Employee", "Apply Leave", "My Leaves"])

    with tab1:
        st.subheader("Register Employee")
        name = st.text_input("Name")
        email = st.text_input("Email")

        if st.button("Add Employee"):
            payload = {"name": name, "email": email}
            response = requests.post(f"{API_URL}/employees/", json=payload)
            if response.status_code == 200:
                st.success("Employee added successfully")
            else:
                st.error(response.json())

    with tab2:
        st.subheader("Apply for Leave")

        employees_res = requests.get(f"{API_URL}/employees/")
        employees = employees_res.json() if employees_res.status_code == 200 else []

        if employees:
            employee_map = {f"{emp['id']} - {emp['name']}": emp["id"] for emp in employees}
            selected_employee = st.selectbox("Select Employee", list(employee_map.keys()))
            employee_id = employee_map[selected_employee]

            leave_type = st.selectbox("Leave Type", ["Sick Leave", "Casual Leave", "Annual Leave"])
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            reason = st.text_area("Reason")

            if st.button("Apply Leave"):
                payload = {
                    "employee_id": employee_id,
                    "leave_type": leave_type,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "reason": reason
                }
                response = requests.post(f"{API_URL}/leaves/", json=payload)
                if response.status_code == 200:
                    st.success("Leave applied successfully")
                else:
                    st.error(response.json()["detail"])
        else:
            st.info("No employees found. Please add an employee first.")

    with tab3:
        st.subheader("View My Leaves")

        employees_res = requests.get(f"{API_URL}/employees/")
        employees = employees_res.json() if employees_res.status_code == 200 else []

        if employees:
            employee_map = {f"{emp['id']} - {emp['name']}": emp["id"] for emp in employees}
            selected_employee = st.selectbox("Choose Employee", list(employee_map.keys()), key="view_leave")
            employee_id = employee_map[selected_employee]

            response = requests.get(f"{API_URL}/employees/{employee_id}/leaves")
            if response.status_code == 200:
                leaves = response.json()
                if leaves:
                    st.dataframe(pd.DataFrame(leaves))
                else:
                    st.info("No leave requests found.")

elif menu == "Admin":
    st.header("Admin Panel")

    response = requests.get(f"{API_URL}/leaves/")
    if response.status_code == 200:
        leaves = response.json()

        if leaves:
            df = pd.DataFrame(leaves)
            st.dataframe(df)

            leave_ids = [leave["id"] for leave in leaves if leave["status"] == "Pending"]

            if leave_ids:
                selected_leave_id = st.selectbox("Select Pending Leave ID", leave_ids)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Approve"):
                        res = requests.put(f"{API_URL}/leaves/{selected_leave_id}/approve")
                        if res.status_code == 200:
                            st.success("Leave approved")
                        else:
                            st.error(res.json()["detail"])

                with col2:
                    if st.button("Reject"):
                        res = requests.put(f"{API_URL}/leaves/{selected_leave_id}/reject")
                        if res.status_code == 200:
                            st.success("Leave rejected")
                        else:
                            st.error(res.json()["detail"])
            else:
                st.info("No pending leave requests.")
        else:
            st.info("No leave requests found.")