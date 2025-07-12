# 💸 Expense Management System

This project is a simple **expense tracking system** built with a **three-tier architecture**:
- **Backend:** FastAPI server for handling API requests and database operations.
- **Frontend:** Streamlit app for a user-friendly interface.
- **Database:** Stores expense records with support for adding, updating, and analyzing expenses.

---

## 📂 **Project Structure**

- **`frontend/`** — Contains the Streamlit application code.
- **`backend/`** — Contains the FastAPI server code and database integration.
- **`requirements.txt`** — Lists all the required Python packages.
- **`README.md`** — Provides an overview of the project, setup instructions, and usage.

---

## 🚀 **Setup Instructions**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/expense-management-system.git
   cd expense-management-system

2. **Install dependencies:** 
    ```commandline
   pip install -r requirements.txt
   ```
   
3. **Run the FastAPI Server:**
    ```commandline
   uvicorn server:app --reload
   ```
   
4. **Run the Streamlit frontend:**
   ```commandline
      streamlit run frontend/app.py
      ```

