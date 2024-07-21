// Copyright (c) 2024, VPS Businesssolution and contributors
// For license information, please see license.txt

frappe.query_reports["Custom Branch Stock Out"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(), // Default value to today's date
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(), // Default value to today's date
            "reqd": 1
        },
        {
            "fieldname": "from_warehouse",
            "label": __("From Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            // "default": "AMAL BRANCH JEDDAH - ANTC", // Default value to specified warehouse
            // "reqd": 1
        },
        {
            "fieldname": "warehouse",
            "label": __("To Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            // "default": "AMAL BRANCH JEDDAH - ANTC", // Default value to specified warehouse
            // "reqd": 1
        },
        {
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "get_query": function() {
                // If item filter is manually entered, apply the filter, otherwise no need to filter by item
                if (frappe.query_report.get_filter_value('item')) {
                    return {
                        query: "erpnext.controllers.queries.item_query"
                    };
                }
            }
        }
    ]

};
