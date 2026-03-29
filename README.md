# Inventory Management FastAPI

Backend Inventory Management REST API built with FastAPI and MySQL featuring CRUD operations, filtering, and database integration.

---

## 🚀 Features

- Create, read, update, and delete inventory items
- Filter inventory data based on price, quantity, and availability
- MySQL database integration using SQLAlchemy
- API testing using Swagger UI

---

## 🛠 Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL

---

## 📂 Project Structure
# 📦 Inventory Management FastAPI

Backend Inventory Management REST API built using FastAPI and MySQL, supporting CRUD operations, filtering, and database integration.

---

## 🚀 Features

- Create, read, update, and delete inventory items  
- Filter inventory data based on price, quantity, and availability  
- MySQL database integration using SQLAlchemy  
- API testing using Swagger UI  

---

## 🛠 Tech Stack

- Python  
- FastAPI  
- SQLAlchemy  
- MySQL  

---

## 📂 Project Structure

inventory-management-fastapi/
├── backend/
│ ├── main.py
│ ├── database.py
│ ├── database_model.py
│ └── models.py
├── .gitignore
├── LICENSE
└── README.md

## ⚙️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/RajveerSingh44222/inventory-management-fastapi.git
cd inventory-management-fastapi

# Create virtual environment
py -m venv myenv
.\myenv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pymysql

# Run the server
python -m uvicorn backend.main:app --reload
