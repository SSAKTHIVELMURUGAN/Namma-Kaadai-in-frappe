# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pypika import functions as fn

class Investment(Document):
	def on_submit(self):
		shop_cashflow = frappe.new_doc('Shop CashFlow')
		shop_cashflow.shop_name = self.shop_name
		shop_cashflow.date = self.date
		shop_cashflow.transaction_id = 'Investment'
		shop_cashflow.transaction_type = self.name
		shop_cashflow.total = self.investment
		shop_cashflow.insert()
	
	# def calculate_all_investment_amount(self):
	# 	# purchase_amount = frappe.db.sql("SELECT SUM(total) FROM `tabShop CashFlow` WHERE transaction_id = %s AND iscancelled = %s",('Purchase', 0,))
	# 	# sale_amount = frappe.db.sql("SELECT SUM(total) FROM `tabShop CashFlow` WHERE transaction_id = %s AND iscancelled = %s",('Sale', 0,))
	# 	# investment_amount = frappe.db.sql("SELECT SUM(total) FROM `tabShop CashFlow` WHERE transaction_id = %s AND iscancelled = %s",('Investment', 0,))
		
	# 	purchase_amount_doc = frappe.qb.DocType("Shop CashFlow")
	# 	purchase_amount = (
	# 		frappe.qb.from_(purchase_amount_doc)
	# 		.select(fn.Sum(purchase_amount_doc.total))
	# 		.where((purchase_amount_doc.transaction_id == 'Purchase') & (purchase_amount_doc.iscancelled == 0))
	# 	)

	# 	sale_amount_doc = frappe.qb.DocType("Shop CashFlow")
	# 	sale_amount = (
	# 		frappe.qb.from_(sale_amount_doc)
	# 		.select(fn.Sum(sale_amount_doc.total))
	# 		.where((sale_amount_doc.transaction_id == 'Sale') & (sale_amount_doc.iscancelled == 0))
	# 	)

	# 	investment_amount_doc = frappe.qb.DocType("Shop CashFlow")
	# 	investment_amount = (
	# 		frappe.qb.from_(investment_amount_doc)
	# 		.select(fn.Sum(investment_amount_doc.total))
	# 		.where((investment_amount_doc.transaction_id == 'Investment') & (investment_amount_doc.iscancelled == 0))
	# 	)

	# 	# if purchase_amount > investment_amount:
	# 	# 	frappe.throw(f"Please purchase within your investment ${investment_amount}")
		
	# 	# main_balance = investment_amount + sale_amount - purchase_amount