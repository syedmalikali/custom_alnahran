import frappe 

@frappe.whitelist()
def get_last_purchaseand_stock_rate(item_code, warehouse):
    purchase_entries = frappe.db.get_all("Purchase Invoice Item",
                                      filters={'item_code': item_code, 'docstatus':1, 'parenttype':"Purchase Invoice", "warehouse": warehouse},
                                      fields=['rate'],
                                      order_by='creation desc',
                                      limit=1)
                                      
    stock_entries = frappe.db.get_all("Stock Entry Detail",
                                      filters={'item_code': item_code, 'docstatus':1, "t_warehouse": warehouse},
                                      fields=['basic_rate'],
                                      order_by='creation desc',
                                      limit=1)

    return (purchase_entries[0].rate if purchase_entries else 0) , (stock_entries[0].basic_rate if stock_entries else 0)
