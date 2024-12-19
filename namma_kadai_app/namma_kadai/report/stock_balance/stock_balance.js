// Copyright (c) 2024, Sakthi and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "shop_name",
			"label": __("Shop Name"),
			"fieldtype": "Link",
			"options": "Shop", 
			"width": "150"
		},
		{
			"fieldname": "item_name",
			"label": __("Item Code"),
			"fieldtype": "Link",
            "options": "Add Item",  
			"width": "150"
		}
	]
};
