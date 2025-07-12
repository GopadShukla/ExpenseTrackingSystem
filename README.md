# Expense Management System

### This projects to use to track the expense which has been developed using three tier, i.e, backend,frontend and a database.

#### Project Structure:

- **frontend/**- Contains the Streamlit application code.
- **backend/**-  Contains the FastAPI server code.
- **requirements.txt/**- Lists all the project's required packages.
- **readme/**- Provides an overview of the project.

## Setup Instructions:

1. **Clone the repository:**
    ```
   git clone https://github.com/'your-user-name'/expense-management-system
   cd expense-management-system
   ```
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

