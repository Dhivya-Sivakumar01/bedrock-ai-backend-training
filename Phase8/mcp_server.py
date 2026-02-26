from strands import tool
from mcp.server.fastmcp import FastMCP
import requests
import uvicorn

API_BASE = "http://localhost:8000"

mcp = FastMCP("employee-mcp")

@mcp.tool()
def create_employee(name: str, role: str):
    """
    Create a new employee.
    Role must be 'Engineer' or 'Associate Engineer'.
    """
    response = requests.post(
        f"{API_BASE}/employees",
        json={"name": name, "role": role},
    )

    return response.json()

@mcp.tool()
def get_employees():
    """
    Retrieve all employees.
    """
    response = requests.get(f"{API_BASE}/employees")
    return response.json()


@mcp.tool()
def get_employee_by_id(employee_id: int):
    """
    Retrieve a specific employee by ID.
    """
    response = requests.get(f"{API_BASE}/employees/{employee_id}")
    return response.json()

@mcp.tool()
def update_employee(employee_id: int, role: str):
    """
    Update employee role.
    """
    response = requests.patch(
        f"{API_BASE}/employees/{employee_id}",
        json={"role": role},
    )

    return response.json()

@mcp.tool()
def delete_employee(employee_id: int):
    """
    Delete employee by ID.
    """
    response = requests.delete(
        f"{API_BASE}/employees/{employee_id}"
    )

    return response.json()

@mcp.tool()
def get_employee_by_name(name: str):
    """
    Retrieve employee by name.
    """
    response = requests.get(f"{API_BASE}/employees/by-name/{name}")
    return response.json()

if __name__ == "__main__":
    print("Starting MCP server on port 3000...")
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=3000)