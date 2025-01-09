# Copyright (c) 2024, Sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from pypika import functions as fn
import csv, json, os
from frappe.utils import get_site_path, get_url, validate_email_address

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
            # purchased_qty = frappe.db.sql("SELECT SUM(quantity) AS remaining_qty FROM `tabTransaction` WHERE shop_name = %s AND item_name = %s AND is_cancel = 0", (self.shop_name, item_name), as_dict=True)
            
            purchased_qty_dict = frappe.qb.DocType("Transaction")

            purchased_qty = (
                frappe.qb.from_(purchased_qty_dict)
                .select(fn.Sum(purchased_qty_dict.quantity).as_("remaining_qty"))
                .where((purchased_qty_dict.shop_name == self.shop_name) & (purchased_qty_dict.item_name == item.item_name) & (purchased_qty_dict.is_cancel == 0) ) 
            ).run(as_dict=True)
            
            
            if purchased_qty and purchased_qty[0]['remaining_qty']:
                available_qty = purchased_qty[0]['remaining_qty']
            else:
                available_qty = 0
            if available_qty == 0:   
                frappe.throw(f"Please Purchase it first {item_name}")
            if abs(sale_qty) > available_qty:  
                frappe.throw(f"Cannot sell {sale_qty}. Only {available_qty} available.")


    def on_cancel(self):
        transaction_list = frappe.get_list('Transaction',
        filters={'id': self.name},
        fields=['name','is_cancel'])
        for transaction in transaction_list:
            transaction_doc = frappe.get_doc('Transaction',transaction['name'])
            transaction_doc.is_cancel = 1
            transaction_doc.save()

        cash_flows = frappe.get_list('Shop CashFlow',   
        filters={'transaction_type': self.name},  
        fields=['name','iscancelled'])
        for cash_flow in cash_flows:
            cash_flow_doc = frappe.get_doc('Shop CashFlow', cash_flow['name'])
            cash_flow_doc.iscancelled = 1
            cash_flow_doc.save()

@frappe.whitelist()
def data_export(selected_fields,docname):
    selected_fields = json.loads(selected_fields)   # convert anyform to dict 
    child_table_data = []
    parent_data = []
    
    for data in selected_fields:
        if data and "." in data:  
            child_data = data.split(".")[1]      # here [1] shows second index in 1st index it has child table name
            child_table_data.append(child_data)  
        else:
            parent_data.append(data)  

    sale_data_db = frappe.qb.DocType("Sale")
    sale_data_item_db = frappe.qb.DocType("Item")

    sale_data_parent = {}
    sale_data_child = {}

    if parent_data:
        sale_data_parent = (
                frappe.qb.from_(sale_data_db)   
                .select(*parent_data)
        ).run(as_dict = True)

    if child_table_data:
        # sale data only on current doc report to show item
        
        sale_data_child = (
                frappe.qb.from_(sale_data_item_db)
                .select(*child_table_data)
                .where((sale_data_item_db.parenttype == 'Sale') & (sale_data_item_db.parent == docname))
        ).run(as_dict = True)

    # check if the child table is not selected
    if sale_data_child and sale_data_parent:        
        data_export_xl = sale_data_child+sale_data_parent
    elif sale_data_child:
        data_export_xl = sale_data_child
    else:
        data_export_xl = sale_data_parent

    return generate_csv(data_export_xl)

def generate_csv(data):
    if not data:
        frappe.msgprint("No data to export")
        return None

    fieldnames = set()
    for row in data:
        fieldnames.update(row.keys())

    # Generate file path
    file_path = get_site_path("private", "files", "mycsvfile.csv")

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    # Make file accessible by Frappe if needed
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": "mycsvfile.csv",
        "is_private": 0,  # 0 = public , 1= private
        "content": open(file_path, "rb").read()
    })  
    
    file_doc.save(ignore_permissions=True)

    return file_doc.file_url  # Return the file URL instead of path


@frappe.whitelist()
def send_email(sender, recipients, subject, file_url):
    # Validate recipient email address
    if not validate_email_address(recipients):
        return "Email error"

    # Send the email with attachment using the relative file URL
    send_email_result = frappe.sendmail(
        recipients=recipients,
        sender=sender,
        subject=subject,
        attachments=[{
        'file_url': file_url  # Use the relative file URL
        }]
    )

    # Log the result of the email sending attempt
    if send_email_result:
        return "success"
    
