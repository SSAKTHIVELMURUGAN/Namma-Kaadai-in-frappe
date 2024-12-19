
// Copyright (c) 2024, Sakthi and contributors
// For license information, please see license.txt

frappe.query_reports["Item wise purchase history"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "reqd": 0
        },
        {
            "fieldname": "item_name",
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Add Item",  
            "reqd": 0
        },
        {
            "fieldname": "shop_name",
            "label": __("Shop Name"),
            "fieldtype": "Link",
            "options": "Shop", 
            "reqd": 0
        }
    ]
}
