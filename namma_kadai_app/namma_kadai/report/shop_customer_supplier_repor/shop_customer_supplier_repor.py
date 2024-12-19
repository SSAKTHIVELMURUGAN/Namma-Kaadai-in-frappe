# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define columns
    columns = get_columns()
    # Fetch data
    data = get_data()
    return columns, data

def get_columns():
    return [
        {"label": "Shop Name", "fieldtype": "Data", "width": 200},
        {"label": "Customer Name", "fieldtype": "Data", "width": 200},
        {"label": "Supplier Name", "fieldtype": "Data", "width": 200},
    ]

def get_data():
    # Fetch shop details along with customer and supplier details
    data = frappe.db.sql("""
        SELECT 
            shop_name,
            GROUP_CONCAT(DISTINCT CASE WHEN party_type = 'Customer' THEN party ELSE NULL END) AS customer_name,
            GROUP_CONCAT(DISTINCT CASE WHEN party_type = 'Supplier' THEN party ELSE NULL END) AS supplier_name
        FROM `tabTransaction`
        WHERE is_cancel = 0
        GROUP BY shop_name
    """, as_list=True)

    return data
