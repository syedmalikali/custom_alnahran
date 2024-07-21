import frappe

@frappe.whitelist()
def get_last_transfer_stock_details(item_code, s_warehouse, t_warehouse):
    
    stock_details = frappe.get_all("Stock Entry Detail",
        {
            "item_code": item_code,
            "s_warehouse": s_warehouse,
            "t_warehouse": t_warehouse,
            "docstatus": 1
        },
        [
            "parent",
            "qty",
            "basic_rate"
        ],
        order_by = 'modified desc',
        limit = 5
    )

    return stock_details

def validate(self, event):
    self.custom_last_transfer_details_ = []
    self.custom_last_transfer_details_warehouse_wise = []

def on_submit(self, event):

    if self.purpose == "Material Transfer":

        if not self.from_warehouse:

            frappe.throw("From Warehouse is mandatory", title = "Message")

        if not self.to_warehouse:

            frappe.throw("To Warehouse is mandatory", title = "Message")

        from_branch = frappe.get_value("Warehouse", self.from_warehouse, "custom_branch")

        to_branch = frappe.get_value("Warehouse", self.to_warehouse, "custom_branch")

        if not from_branch:
            frappe.throw(f"Branch not found in warehouse {self.from_warehouse}", title = "Message")

        if not to_branch:
            frappe.throw(f"Branch not found in warehouse {self.to_warehouse}", title = "Message")

        debit_account = frappe.get_value("Custom Settings JE Table", {"parenttype": "Custom Settings", "branch": from_branch}, "from_account")

        credit_account = frappe.get_value("Custom Settings JE Table", {"parenttype": "Custom Settings", "branch": to_branch}, "to_account")

        if not debit_account:
            frappe.throw(f"Debit Account not found for branch {from_branch}", title = "Message")

        if not credit_account:
            frappe.throw(f"Credit Account not found for branch {to_branch}", title = "Message")

        new_je_doc = frappe.new_doc("Journal Entry")

        new_je_doc.voucher_type = "Journal Entry"
        new_je_doc.company = self.company
        new_je_doc.posting_date = self.posting_date
        new_je_doc.custom_stock_transfer_reference = self.name
        new_je_doc.append("accounts", {
            "account": debit_account,
            "debit_in_account_currency": self.total_outgoing_value
        })
        new_je_doc.append("accounts", {
            "account": credit_account,
            "credit_in_account_currency": self.total_outgoing_value
        })

        new_je_doc.save()
        new_je_doc.submit()

@frappe.whitelist()
def get_last_transfer_stock_details_warehoue_wise(item_code, s_warehouse):

    stock_details = []

    warehouse_list = frappe.get_all("Warehouse", {"is_group": 0, "disabled": 0, "name": ["!=", s_warehouse]}, pluck = "name")

    for t_warehouse in warehouse_list:

        stock_detail = frappe.get_all("Stock Entry Detail",
            {
                "item_code": item_code,
                "s_warehouse": s_warehouse,
                "t_warehouse": t_warehouse,
                "docstatus": 1
            },
            [
                "parent",
                "qty",
                "t_warehouse as warehouse",
                "basic_rate"
            ],
            order_by = 'modified desc',
            limit = 1
        )

        if stock_detail:
            stock_details.append(stock_detail[0])

    return stock_details