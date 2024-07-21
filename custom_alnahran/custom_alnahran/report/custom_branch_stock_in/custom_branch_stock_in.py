# Copyright (c) 2024, VPS Businesssolution and contributors
# For license information, please see license.txt

# Import necessary modules
import frappe

# Import translation function
from frappe import _

def execute(filters=None):
    # Define columns and data list
    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "align": "left"},
        # {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data"},
        {"label": "Voucher No", "fieldname": "voucher_no", "fieldtype": "Link", "options": "Stock Entry"},
        {"label": "UOM", "fieldname": "stock_uom", "fieldtype": "Data"},
        {"label": "Qty", "fieldname": "in_qty", "fieldtype": "Float"},
        {"label": "Rate", "fieldname": "basic_rate", "fieldtype": "Currency"}
        # {"label": "From Warehouse", "fieldname": "s_warehouse", "fieldtype": "Link", "options": "Warehouse"},
        # {"label": "To Warehouse", "fieldname": "to_warehouse", "fieldtype": "Link", "options": "Warehouse"},
        
        
    ]
    
    data = []

    # Get default values for from_date and to_date
    from_date = filters.get("from_date") or frappe.utils.today()
    to_date = filters.get("to_date") or frappe.utils.today()

    # Query to fetch data from Stock Entry Detail table
    query = """
        SELECT
            sed.item_code,
            sed.item_name,
            sed.stock_uom,
            sed.qty AS in_qty,
            sed.basic_rate,
            sed.s_warehouse,  -- Using correct field name for From Warehouse
            sed.t_warehouse AS to_warehouse,
            se.name AS voucher_no,
            se.posting_date AS date
        FROM
            `tabStock Entry` se
        INNER JOIN
            `tabStock Entry Detail` sed ON se.name = sed.parent
        WHERE
            se.docstatus = 1
            AND (se.purpose = 'Material Transfer' OR se.purpose = 'Stock Transfer')
            AND se.posting_date BETWEEN %(from_date)s AND %(to_date)s
    """

    # Filter parameters
    filter_params = {
        "from_date": from_date,
        "to_date": to_date
    }

    # If warehouse filter is provided and not empty, add it to the query
    if filters and filters.get("warehouse"):
        query += " AND sed.t_warehouse = %(warehouse)s"
        filter_params["warehouse"] = filters["warehouse"]
    else:  # If warehouse filter is empty or not provided, fetch data for all warehouses
        query += " AND 1=1"

    # If from_warehouse filter is provided and not empty, add it to the query
    if filters and filters.get("from_warehouse"):
        query += " AND sed.s_warehouse = %(from_warehouse)s"
        filter_params["from_warehouse"] = filters["from_warehouse"]

    # If item filter is provided and not empty, add it to the query
    if filters and filters.get("item"):
        query += " AND sed.item_code = %(item)s"
        filter_params["item"] = filters["item"]

    # Fetch data from database
    results = frappe.db.sql(query, filter_params, as_dict=True)

    # Populate data for each row in the report
    for row in results:
        data.append({
            "item_code": row.item_code,
            "item_name": row.item_name,
            "stock_uom": row.stock_uom,
            "in_qty": row.in_qty,
            "basic_rate": row.basic_rate,
            "s_warehouse": row.s_warehouse,
            "to_warehouse": row.to_warehouse,
            "voucher_no": row.voucher_no,
            "date": row.date
        })

    return columns, data
