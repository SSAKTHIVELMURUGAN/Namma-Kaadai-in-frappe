# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    frappe.errprint(filters)
    columns = [
        {
            "fieldname": "date",
            "fieldtype": "Date",
            "label": "Date",
            "width": 100
        },
        {
            "fieldname": "shop_name",
            "fieldtype": "Data",
            "label": "Shop Name",
            "width": 100
        },
        {
            "fieldname": "suppiler_name",
            "fieldtype": "Data",
            "label": "Supplier Name",
            "width": 100
        },
        {
            "fieldname": "item_name",
            "fieldtype": "Data",
            "label": "Item Code",
            "width": 100
        },
        {
            "fieldname": "rate",
            "fieldtype": "Int",
            "label": "Rate",
            "width": 100
        },
        {
            "fieldname": "quantity",
            "fieldtype": "Int",
            "label": "Quantity",
            "width": 100
        },
        {
            "fieldname": "amount",
            "fieldtype": "Int",
            "label": "Amount",
            "width": 100
        }
    ]
    data = get_data(filters)
    return columns, data


def get_data(filters):
    purchase = frappe.qb.DocType("Purchase")
    item = frappe.qb.DocType("Item")

    q = (
         frappe.qb.from_(purchase)
         .select(purchase.date, purchase.shop_name, purchase.suppiler_name, item.item_name, item.rate, item.quantity, item.amount)
         .inner_join(item)
         .on(purchase.name == item.parent)
         .where(purchase.docstatus==1)
        )

    # sql = "SELECT purchase.date, purchase.shop_name, purchase.suppiler_name, item.item_name, item.rate, item.quantity, item.amount FROM `tabPurchase` AS purchase INNER JOIN `tabItem` AS item ON purchase.name = item.parent WHERE purchase.docstatus=1"
    
    if filters.get("date"):
        q = q.where(purchase.date == filters["date"])
        # sql += " AND purchase.date = %(date)s"
    if filters.get("shop_name"):
        q = q.where(purchase.shop_name == filters['shop_name'])
        # sql += " AND purchase.shop_name = %(shop_name)s"
    if filters.get("item_name"):
        q = q.where(item.item_name == filters['item_name'])
        # sql += " AND item.item_name = %(item_name)s"
    result = q.run(as_dict = True)
    # return frappe.db.sql(sql, filters, as_dict=True)
    return result