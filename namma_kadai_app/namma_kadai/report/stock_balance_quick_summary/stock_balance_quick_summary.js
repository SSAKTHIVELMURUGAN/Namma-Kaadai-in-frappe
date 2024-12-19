// Copyright (c) 2024, Sakthi and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance Quick Summary"] = {
    "filters": [
        {
            "fieldname": "shop_name",
            "label": __("Shop Name"),
            "fieldtype": "Link",
            "options": "Shop", 
            "reqd": 0
        },
        {
            "fieldname": "item_name",  
            "label": __("Item Code"),
            "fieldtype": "Link",
            "options": "Add Item",  
            "reqd": 0  
        },
    ]
}
