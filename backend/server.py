from fastapi import FastAPI, Request
from datetime import date
import db_integration
from pydantic import BaseModel
from typing import List
from mysql.connector import Error as MySQLError
from fastapi.responses import JSONResponse
import logging

app=FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Exception handler for MySQL errors
@app.exception_handler(MySQLError)
async def mysql_error_handler(request: Request, exc: MySQLError):
    logger.error(f"MySQL error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Please try again later."}
    )

# Exception handler for ValueErrors
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

# Catch-all fallback exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

class Expense(BaseModel):
    id:int
    amount:float
    category:str
    notes:str

class DateRange(BaseModel):
    start_date:date
    end_date:date



@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expense_by_date(expense_date:date):
    expenses=db_integration.fetch_expense_by_date(expense_date)
    response=[]
    for i in expenses:
        response.append({
        "id":i[0],
        "amount": i[2],
        "category": i[3],
        "notes": i[4]})

    return response


@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date:date,expenses:List[Expense]):
    for expense in expenses:
        db_integration.insert_expense(expense_date,expense.amount,expense.category,expense.notes)

    return "Expense inserted successfully!"

@app.post("/analytics")
def get_analytics_by_date_range(date_range:DateRange):
    response=db_integration.fetch_expense_between_dates(date_range.start_date,date_range.end_date)

    # return response
    total_sum = 0
    total_sum=sum([category['total_sum'] for category in response])
    breakdown={}
    for row in response:
        percentage=(row["total_sum"]/total_sum)*100 if row["total_sum"]!=0 else 0
        # breakdown={row["category"]:{"total":row["total_sum"],"percentage":percentage}}
        breakdown.update({row["category"]: {"total": row["total_sum"], "percentage": percentage}})

    return breakdown


@app.put("/expenses/{expense_id}")
def update_expense(expense_id:int,expense:Expense):
    db_integration.update_expense_by_id(
        expense_id,
        expense.amount,
        expense.category,
        expense.notes
    )
    return {"detail": f"Expense ID {expense_id} updated successfully"}