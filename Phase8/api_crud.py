from db import get_connection
from fastapi import FastAPI, HTTPException
import mysql.connector
from schemas import EmployeeCreate, EmployeeResponse

app = FastAPI()

@app.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO employees (name, role) VALUES (%s, %s)",
            (employee.name, employee.role),
        )
        conn.commit()

        new_id = cursor.lastrowid

        return EmployeeResponse(
            id=new_id,
            name=employee.name,
            role=employee.role,
        )

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees WHERE id=%s", (employee_id,))
    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee

@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, role: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if role is None:
        raise HTTPException(status_code=400, detail="Nothing to update")

    cursor.execute(
        "UPDATE employees SET role=%s WHERE id=%s",
        (role, employee_id),
    )
    conn.commit()

    cursor.execute("SELECT * FROM employees WHERE id=%s", (employee_id,))
    updated_employee = cursor.fetchone()

    cursor.close()
    conn.close()

    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return updated_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"status": "deleted", "id": employee_id}

@app.get("/employees/by-name/{name}", response_model=list[EmployeeResponse])
def get_employee(name: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"SELECT * FROM employees WHERE name LIKE '%{name}%'")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    if not employees:
        raise HTTPException(status_code=404, detail="No employees found matching that name")

    return employees