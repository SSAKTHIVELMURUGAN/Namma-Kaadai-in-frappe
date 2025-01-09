# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe
from pypika import Case,functions as fn
from frappe.query_builder.functions import GroupConcat

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
    # GroupConcat = CustomFunction("GROUP_CONCAT",["string"])
    transaction_doc_list = frappe.qb.DocType("Transaction")

    customer_case = (
        Case()
        .when(transaction_doc_list.party_type == 'Customer', transaction_doc_list.party)
        .else_(None)
    )
    supplier_case = (
        Case()
        .when(transaction_doc_list.party_type == 'Supplier', transaction_doc_list.party)
        .else_(None)
    )


    data = (
        frappe.qb.from_(transaction_doc_list)   
        .select(
            transaction_doc_list.shop_name,
            GroupConcat(customer_case).distinct().as_("customer_name"),
            GroupConcat(supplier_case).distinct().as_("supplier_name")
        )
        .where(transaction_doc_list.is_cancel == 0)
        .groupby(transaction_doc_list.shop_name)
    ).run(as_list=True)

    # data = frappe.db.sql("""
    #     SELECT 
    #         shop_name,
    #         GROUP_CONCAT(DISTINCT CASE WHEN party_type = 'Customer' THEN party ELSE NULL END) AS customer_name,
    #         GROUP_CONCAT(DISTINCT CASE WHEN party_type = 'Supplier' THEN party ELSE NULL END) AS supplier_name
    #     FROM `tabTransaction`
    #     WHERE is_cancel = 0
    #     GROUP BY shop_name
    # """, as_list=True)

    return data
