# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sale(Document):
    def validate(self):
        # calculate total amount and each amount for each item and display in front end after save
        self.total_amount()
            
    def on_submit(self):
        # sale qty
        self.check_avaible_qty()
        # update automatically in transaction doctype for every single item
        self.transaction_doc_type()
        # in shop cash flow doctype -- to track cash flow
        self.shop_cash_flow_doc_type()


    def total_amount(self):
        self.total = 0
        for row in self.item_list:
            row.amount = row.quantity * row.rate
            self.total += row.amount

    def transaction_doc_type(self):
        for item in self.item_list:
            transaction = frappe.new_doc('Transaction')  
            transaction.status = 'Sale'  
            transaction.party_type = 'Customer'
            transaction.party = self.customer_name
            transaction.shop_name = self.shop_name  
            transaction.date = self.date  
            transaction.item_name = item.item_name  
            transaction.quantity = item.quantity * -1
            transaction.rate = item.rate  
            transaction.total = item.quantity * item.rate
            transaction.id = self.name  
            transaction.insert()

    def shop_cash_flow_doc_type(self):
        shop_cashflow = frappe.new_doc('Shop CashFlow')
        shop_cashflow.shop_name = self.shop_name
        shop_cashflow.date = self.date
        shop_cashflow.transaction_id = 'Sale'
        shop_cashflow.transaction_type = self.name
        shop_cashflow.total = self.total
        shop_cashflow.insert()

    def check_avaible_qty(self):
        for item in self.item_list:  
            item_name = item.item_name  
            sale_qty = item.quantity 
            purchased_qty = frappe.db.sql("SELECT SUM(quantity) AS remaining_qty FROM `tabTransaction` WHERE shop_name = %s AND item_name = %s AND is_cancel = 0", (self.shop_name, item_name), as_dict=True)
            if purchased_qty and purchased_qty[0]['remaining_qty']:
                available_qty = purchased_qty[0]['remaining_qty']
            else:
                available_qty = 0
            if available_qty == 0:   
                frappe.throw(f"Please Purchase it first {item_name}")
            if abs(sale_qty) > available_qty:  
                frappe.throw(f"Cannot sell {sale_qty}. Only {available_qty} available.")