import frappe

@frappe.whitelist()
def get_latest_item_code():
    latest_item = frappe.get_list('Item', filters={}, order_by='creation DESC', limit_page_length=1)
    if latest_item:
        return latest_item[0].name
    return None

@frappe.whitelist()
def get_next_item_code():
    latest_item_code = get_latest_item_code()
    if latest_item_code:
        last_item_number = int(latest_item_code)
        new_item_number = last_item_number + 1
        return str(new_item_number)
    return None

