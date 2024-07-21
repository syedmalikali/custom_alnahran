// Copyright (c) 2024, VPS Businesssolution and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Warehouse Wise Stock Balance"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            reqd: 1,
            default: frappe.defaults.get_user_default("Company"),
        },
        {
            fieldname: "today_date",
            label: __("Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(), // Default value to today's date
            reqd: 1
        },
        {
            fieldname: "item_code",
            label: __("Item"),
            fieldtype: "Link",
            options: "Item",
            reqd: 0 // This makes the item code filter optional
        }
    ],
};
