import frappe
from datetime import datetime

# Define the function to fetch stock balance and quantity for each item in each warehouse within the specified date range
def get_stock_balance_and_quantity(filters):
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    query = """
        SELECT
            i.item_code,
            i.item_name,
            SUM(CASE WHEN b.warehouse = 'DAMMAM BRANCH - ANTC' THEN b.actual_qty ELSE 0 END) AS 'DAMMAM BRANCH - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'MAIN WAREHOUSE - ANTC' THEN b.actual_qty ELSE 0 END) AS 'MAIN WAREHOUSE - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'KHAMIS BRANCH - ANTC' THEN b.actual_qty ELSE 0 END) AS 'KHAMIS BRANCH - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'VANSALE-1 - ANTC' THEN b.actual_qty ELSE 0 END) AS 'VANSALE-1 - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'VANSALE-2 - ANTC' THEN b.actual_qty ELSE 0 END) AS 'VANSALE-2 - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'LIFETIME NAJRAN - ANTC' THEN b.actual_qty ELSE 0 END) AS 'LIFETIME NAJRAN - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'LIFETIME-2 KHAMIS - ANTC' THEN b.actual_qty ELSE 0 END) AS 'LIFETIME-2 KHAMIS - ANTC Qty',
            SUM(CASE WHEN b.warehouse = 'LIFETIME-1 KHAMIS - ANTC' THEN b.actual_qty ELSE 0 END) AS 'LIFETIME-1 KHAMIS - ANTC Qty',
            SUM(b.actual_qty) AS 'Total Qty'
        FROM
            `tabItem` i
        LEFT JOIN
            `tabBin` b ON i.item_code = b.item_code
        GROUP BY
            i.item_code
        ORDER BY
            i.item_code
    """
    
    # Execute the query with parameters
    results = frappe.db.sql(query, {"today_date": today_date}, as_dict=True)
    
    # Return the results
    return results

# Define the main function to generate the report
def warehouse_wise_stock_balance(filters):
    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 150},
        {"label": "DAMMAM BRANCH - ANTC Qty", "fieldname": "DAMMAM BRANCH - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "MAIN WAREHOUSE - ANTC Qty", "fieldname": "MAIN WAREHOUSE - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "KHAMIS BRANCH - ANTC Qty", "fieldname": "KHAMIS BRANCH - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "VANSALE-1 - ANTC Qty", "fieldname": "VANSALE-1 - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "VANSALE-2 - ANTC Qty", "fieldname": "VANSALE-2 - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "LIFETIME NAJRAN - ANTC Qty", "fieldname": "LIFETIME NAJRAN - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "LIFETIME-2 KHAMIS - ANTC Qty", "fieldname": "LIFETIME-2 KHAMIS - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "LIFETIME-1 KHAMIS - ANTC Qty", "fieldname": "LIFETIME-1 KHAMIS - ANTC Qty", "fieldtype": "Float", "width": 150},
        {"label": "Total Qty", "fieldname": "Total Qty", "fieldtype": "Float", "width": 150}
    ]
    
    # Fetch stock balance and quantity data within the specified date range
    data = get_stock_balance_and_quantity(filters)
    
    # Return the report data
    return columns, data

def execute(filters=None):
    # Your code to execute the report goes here
    columns, data = warehouse_wise_stock_balance(filters)
    return columns, data

