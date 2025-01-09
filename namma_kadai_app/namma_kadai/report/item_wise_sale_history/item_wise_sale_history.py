# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	frappe.errprint(filters)
	columns  = [
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
   "width":100
  },
  {
   "fieldname": "customer_name",
   "fieldtype": "Data",
   "label": "Customer Name",
   "width": 100
  },
  {
   "fieldname": "item_name",
   "fieldtype": "Data",
   "label": "Item Code",
   "width": 0
  },
  {
   "fieldname": "rate",
   "fieldtype": "Int",
   "label": "rate",
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
    sql = "SELECT sale.date, sale.shop_name, sale.customer_name, item.item_name, item.rate, item.quantity, item.amount FROM `tabSale` AS sale INNER JOIN `tabItem` AS item ON sale.name = item.parent WHERE sale.docstatus=1"
    print(sql)
    sale = frappe.qb.DocType("Sale")
    item = frappe.qb.DocType("Item")

    q = (
         frappe.qb.from_(sale)
         .select(sale.date, sale.shop_name, sale.customer_name, item.item_name, item.rate, item.quantity, item.amount)
         .inner_join(item)
         .on(sale.name == item.parent)
         .where(sale.docstatus == 1)
    )

    if filters.get("date"):
        # sql += " AND sale.date = %(date)s"
        q = q.where(sale.date == filters['date'])
    if filters.get("shop_name"):
         q = q.where(sale.shop_name == filters['shop_name'])
        # sql += " AND sale.shop_name = %(shop_name)s"
    if filters.get("item_name"):
         q = q.where(item.item_name == filters['item_name'])
        # sql += " AND item.item_name = %(item_name)s"
    result = q.run(as_dict = True)
    print(frappe.db.sql(sql, filters, as_dict=True))
        
    # return frappe.db.sql(sql, filters, as_dict=True)
    return result