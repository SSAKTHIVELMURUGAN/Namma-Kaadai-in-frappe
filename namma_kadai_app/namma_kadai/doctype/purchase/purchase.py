# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Purchase(Document):
    def validate(self):
        # calculate total amount and each amount for each item and display in front end after save
        self.total_amount()

    def on_submit(self):
        # calculate all purchase amount
        self.calculate_all_purchase_amount()
        # update automatically in transaction doctype for every single item
        self.transaction_doc_type()
        # in shop cash flow doctype -- to track cash flow
        self.shop_cash_flow_doc_type()

    

    def total_amount(self):
        self.total = 0
        for row in self.item_list:
            row.amount = row.quantity * row.rate
            self.total += row.amount

    def calculate_all_purchase_amount(self):
        totals_dict = frappe.db.sql("""
        SELECT 
        SUM(total) AS investment_amount_tab
        FROM `tabShop CashFlow`
        WHERE shop_name = %s
        """, (self.shop_name,), as_dict=True)

        if totals_dict:
            for totals_dict_value in totals_dict:
                investment_amount = totals_dict_value.get('investment_amount_tab',0) or 0
                # sale_amount = totals_dict_value.get('sale_amount_tab',0)
        # investment_amount *= -1
        if self.total > investment_amount:
            frappe.throw(f"Please purchase within your investment ${investment_amount}")

        # investment_amount -= purchase_amount

        # main_balance = investment_amount + sale_amount - purchase_amount

    def transaction_doc_type(self):
        for item in self.item_list:
            transaction = frappe.new_doc('Transaction')  
            transaction.status = 'Purchase'  
            transaction.party_type = 'Supplier'
            transaction.party = self.suppiler_name
            transaction.shop_name = self.shop_name  
            transaction.date = self.date  
            transaction.item_name = item.item_name  
            transaction.quantity = item.quantity 
            transaction.rate = item.rate  
            transaction.total = item.quantity * item.rate
            transaction.id = self.name  
            transaction.insert()

    def shop_cash_flow_doc_type(self):
        shop_cashflow = frappe.new_doc('Shop CashFlow')
        shop_cashflow.shop_name = self.shop_name
        shop_cashflow.date = self.date
        shop_cashflow.transaction_id = 'Purchase'
        shop_cashflow.transaction_type = self.name
        shop_cashflow.total = self.total * -1
        shop_cashflow.insert()