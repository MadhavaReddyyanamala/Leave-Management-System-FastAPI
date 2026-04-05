# Leave-Management-System-FastAPI
Leave Management System (FastAPI + Streamlit + Postgresql)

A full-stack Leave Management System built using FastAPI (backend), Streamlit (frontend) and Postgresql(Database). This application allows employees to apply for leave and administrators to manage, approve, or reject requests efficiently.

#### Problem Statement

In many organizations, leave management is still handled manually using spreadsheets or emails.

This creates several problems:

No proper tracking of leave requests
High chances of errors or overlapping leaves
Lack of transparency between employees and management
Time-consuming approval process

So, the goal of my project is to automate the leave management process with proper validation, tracking, and an easy-to-use interface.

# 🚀 Features

#### 👨‍💼 Employee Module

Register new employees

Apply for leave (Sick, Casual, Annual)

View personal leave history

Validation for:
Past date restriction, 
Overlapping leave requests

#### 🛠️ Admin Module

View all leave requests

Approve or reject leave requests

Manage pending leave applications

# 🏗️ Tech Stack
#### Backend
FastAPI, 
SQLAlchemy ORM, 
PostgreSQL, 
Pydantic (data validation).
#### Frontend
Streamlit, 
Requests, 
Pandas.

# WorkFlow / Architecture
<img width="425" height="831" alt="image" src="https://github.com/user-attachments/assets/ce63f0e2-4558-46cc-bf0d-ab89a48462c9" />

# 📂 Project Structure
<img width="689" height="464" alt="image" src="https://github.com/user-attachments/assets/16070e5f-cd17-4d12-b80c-efd5a3dab178" />

# 🔌 API Endpoints
##### Employee

POST /employees/ → Add employee

GET /employees/ → List employees

##### Leave

POST /leaves/ → Apply leave

GET /leaves/ → Get all leaves

GET /employees/{id}/leaves → Employee leaves

PUT /leaves/{id} → Update leave

DELETE /leaves/{id} → Delete leave

PUT /leaves/{id}/approve → Approve

PUT /leaves/{id}/reject → Reject
