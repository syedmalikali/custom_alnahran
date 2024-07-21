import frappe

@frappe.whitelist()
def fetch_rate_details(item_code, customer):
    rate_details =   frappe.db.sql(f""" select sii.item_code, sii.qty as qty_1, sii.rate, sii.amount, sii.discount_amount, si.posting_date as date, si.customer, si.name as sales_invoice from `tabSales Invoice Item` sii left join `tabSales Invoice` si on si.name = sii.parent where si.customer = '{customer}' and sii.item_code = '{item_code}' and si.is_return = 0 and si.docstatus = 1  order by si.modified limit 5 """,as_dict=1)
    
    # doc_count = 0
    # rate_details = []

    # so_details = frappe.get_all(
    #     'Sales Invoice Item',
    #     ['rate', 'parent'],
    #     {
    #         'item_code': item_code,
    #         'parenttype': 'Sales Invoice',
    #         'docstatus': 1
    #     },
    #     order_by="modified"
    # )

    # for row in so_details[::-1]:
    #     if frappe.db.get_value('Sales Invoice', row.parent, 'docstatus') == 1:
    #         so_doc = frappe.get_doc('Sales Invoice', row.parent)

    #         # Check if the customer matches the specified customer
    #         if so_doc.customer == customer:
    #             rate_details.append(
    #                 {
    #                     'sales_invoice': row.parent,
    #                     'date': so_doc.posting_date,
    #                     'customer': so_doc.customer, 
    #                     'rate': row.rate,
    #                     'qty': row.qty,
    #                     'discount_amount': row.discount_amount,
    #                     'amount': row.amount
    #                 }
    #             )
    #             doc_count += 1
    #         if doc_count == 5:
    #             break

    return rate_details

@frappe.whitelist()
def fetch_purchase_rate_details(item_code, supplier):
    doc_count = 0
    rate_details = []

    pi_details = frappe.get_all(
        'Purchase Invoice Item',
        ['rate', 'parent', 'qty', 'amount', 'discount_amount'],
        {
            'item_code': item_code,
            'parenttype': 'Purchase Invoice',
            'docstatus': 1
        },
        order_by="modified"
    )

    for row in pi_details[::-1]:
        if frappe.db.get_value('Purchase Invoice', row.parent, 'docstatus') == 1:
            pi_doc = frappe.get_doc('Purchase Invoice', row.parent)

           
            if pi_doc.supplier == supplier:
                rate_details.append(
                    {
                        'purchase_invoice': row.parent,
                        'date': pi_doc.posting_date,
                        'supplier': pi_doc.supplier, 
                        'rate': row.rate,
                        'vpsqty': row.qty,
                        'amount': row.amount,
                        'discount_amount': row.discount_amount
                    }
                )
                doc_count += 1
            if doc_count == 5:
                break

    return rate_details